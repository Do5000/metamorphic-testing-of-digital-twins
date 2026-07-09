import pytest
import pytest_asyncio
import asyncio
import json
import os
import glob
from mt_engine.runner import DslRunner
from pytest_dt_mt.relations.base import MetamorphicRelationError
from pytest_dt_mt.core import PreconditionFailedError

# Find all generated JSON files in the framework/dsl folder or its subdirectories
# Assuming the user compiles their .mt files into .json
DSL_OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dsl")

def compile_mt_files():
    import subprocess
    # Find all .mt files in dsl folder, ignoring node_modules
    mt_files = []
    for root, dirs, files in os.walk(DSL_OUT_DIR):
        if "node_modules" in root:
            continue
        for file in files:
            if file.endswith(".mt"):
                mt_files.append(os.path.join(root, file))
                
    if not mt_files:
        return

    env = os.environ.copy()
    # Add common Unix/macOS Node install paths to PATH dynamically using correct path separator
    paths_to_add = []
    if os.name != "nt":
        paths_to_add = ["/opt/homebrew/bin", "/usr/local/bin"]
    
    current_path = env.get("PATH", "")
    new_paths = paths_to_add + ([current_path] if current_path else [])
    env["PATH"] = os.pathsep.join(new_paths)
    
    cli_path = os.path.join("out", "cli", "main.js")
    generated_dir = os.path.join(DSL_OUT_DIR, "generated")
    os.makedirs(generated_dir, exist_ok=True)
    
    for mt_file in mt_files:
        try:
            result = subprocess.run(
                ["node", cli_path, "generate", mt_file, "-d", generated_dir],
                cwd=DSL_OUT_DIR,
                env=env,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"[DSL RUNNER ERROR] Failed to compile {mt_file}: {result.stderr or result.stdout}")
        except Exception as e:
            print(f"[DSL RUNNER ERROR] Exception while compiling {mt_file}: {e}")

# Compile .mt files to .json automatically before test collection
compile_mt_files()

JSON_FILES = glob.glob(os.path.join(DSL_OUT_DIR, "generated", "*.json"))

# Ignore langium configuration files or other non-test json files
def is_test_json(filepath):
    if not os.path.exists(filepath):
        return False
    if "langium-config.json" in filepath or "tsconfig.json" in filepath or "package.json" in filepath or "package-lock.json" in filepath or ".tmLanguage.json" in filepath or "langium-configuration.json" in filepath:
        return False
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return "elements" in data
    except:
        return False

TEST_JSONS = [f for f in JSON_FILES if is_test_json(f)]
SKIPPED_FILES = {}
EXECUTED_FILES = set()

def get_test_cases():
    cases = []
    for filepath in TEST_JSONS:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            for el in data.get("elements", []):
                if el["type"] == "TestDefinition":
                    # Parameterize expects a tuple or list of arguments
                    cases.append(pytest.param(filepath, data, el, id=f"{os.path.basename(filepath)}::{el.get('name', 'Unnamed')}"))
        except Exception:
            pass
    return cases


async def _run_hooks(runner, full_data, hook_type, filepath=None):
    """Helper to execute DSL lifecycle hooks and handle common exceptions."""
    for el in full_data.get("elements", []):
        if el["type"] == "LifecycleHook" and el.get("hookType") == hook_type:
            try:
                await runner.execute_hook(el)
            except PreconditionFailedError as e:
                if hook_type == "beforeAll" and filepath:
                    SKIPPED_FILES[filepath] = f"Precondition in beforeAll failed: {e}"
                    pytest.skip(SKIPPED_FILES[filepath])
                else:
                    pytest.skip(f"Precondition in {hook_type} failed: {e}")
            except Exception as e:
                if hook_type in ("afterEach", "afterAll"):
                    print(f"\n[ERROR] Error in {hook_type} hook: {e}")
                else:
                    raise


@pytest.mark.asyncio
@pytest.mark.parametrize("filepath, full_data, test_data", get_test_cases())
async def test_execute_dsl_scenario(dt_adapter, wait_dt, pytestconfig, filepath, full_data, test_data):
    if filepath in SKIPPED_FILES:
        pytest.skip(SKIPPED_FILES[filepath])
        
    EXECUTED_FILES.add(filepath)
        
    __tracebackhide__ = True
    runner = DslRunner(dt_adapter, full_data)
    
    # Run beforeAll hooks from the same file IF they haven't run yet
    if not full_data.get("_before_all_run", False):
        await _run_hooks(runner, full_data, "beforeAll", filepath)
        full_data["_before_all_run"] = True

    try:
        # Run beforeEach hooks from the same file
        await _run_hooks(runner, full_data, "beforeEach")
                
        # Create a dynamic wait wrapper that prioritizes the adapter's measured latency
        async def dynamic_wait():
            if hasattr(dt_adapter, "_measured_latency") and dt_adapter._measured_latency is not None:
                await asyncio.sleep(dt_adapter._measured_latency)
            else:
                await wait_dt()

        # Run the test definition
        verbose = pytestconfig.getoption("--monitor")
        err_msg = None
        try:
            await runner.execute_test(test_data, dynamic_wait, verbose=verbose)
        except MetamorphicRelationError as e:
            err_msg = str(e)
            
        if err_msg:
            pytest.fail(err_msg, pytrace=False)
    finally:
        # Run afterEach hooks from the same file
        await _run_hooks(runner, full_data, "afterEach")
                    
        # Store/update the measured latency and calibration results for the summary report
        from pytest_dt_mt.fixtures import _MODULE_WAIT_DT, _CALIBRATION_REPORTS
        dsl_key = f"DSL: {os.path.basename(filepath)}"
        if hasattr(dt_adapter, "_measured_latency") and dt_adapter._measured_latency is not None:
            _MODULE_WAIT_DT[dsl_key] = max(_MODULE_WAIT_DT.get(dsl_key, 0.0), dt_adapter._measured_latency)
        if hasattr(dt_adapter, "_calibration_results") and dt_adapter._calibration_results:
            if dsl_key not in _CALIBRATION_REPORTS:
                _CALIBRATION_REPORTS[dsl_key] = []
            for res in dt_adapter._calibration_results:
                if res not in _CALIBRATION_REPORTS[dsl_key]:
                    _CALIBRATION_REPORTS[dsl_key].append(res)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def dsl_after_all_teardown():
    """Executes AfterAll hooks for any DSL files that were run during this session."""
    yield
    from pytest_dt_mt.core import DigitalTwinAdapter
    
    if not EXECUTED_FILES:
        return
        
    adapter = DigitalTwinAdapter()
    runner = DslRunner(adapter, {})
    for filepath in EXECUTED_FILES:
        if not os.path.exists(filepath): continue
        with open(filepath, "r") as f:
            data = json.load(f)
        await _run_hooks(runner, data, "afterAll")
                
    await adapter.close()
