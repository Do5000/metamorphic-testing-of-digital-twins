import pytest
import json
import os
import glob
from mt_engine.runner import DslRunner
from pytest_dt_mt.relations.base import MetamorphicRelationError

# Find all generated JSON files in the framework/dsl folder or its subdirectories
# Assuming the user compiles their .mt files into .json
DSL_OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dsl")
JSON_FILES = glob.glob(os.path.join(DSL_OUT_DIR, "**", "*.json"), recursive=True)

# Ignore langium configuration files or other non-test json files
def is_test_json(filepath):
    if not os.path.exists(filepath):
        return False
    if "langium-config.json" in filepath or "tsconfig.json" in filepath or "package.json" in filepath or "package-lock.json" in filepath or ".tmLanguage.json" in filepath:
        return False
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return "elements" in data
    except:
        return False

TEST_JSONS = [f for f in JSON_FILES if is_test_json(f)]

def get_test_cases():
    cases = []
    for filepath in TEST_JSONS:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                
            for el in data.get("elements", []):
                if el["type"] == "TestDefinition":
                    # Parameterize expects a tuple or list of arguments
                    cases.append(pytest.param(filepath, data, el, id=el.get("name", "Unnamed Test")))
        except Exception:
            pass
    return cases

@pytest.mark.asyncio
async def test_dsl_hooks_before_all(dt_adapter):
    """Executes BeforeAll hooks for the loaded files before the actual tests run.
    Currently runs all BeforeAll hooks found in the JSONs. In a real scenario, this could be scoped per file."""
    runner = DslRunner(dt_adapter, {})
    for filepath in TEST_JSONS:
        if not os.path.exists(filepath): continue
        with open(filepath, "r") as f:
            data = json.load(f)
        for el in data.get("elements", []):
            if el["type"] == "LifecycleHook" and el.get("hookType") == "beforeAll":
                await runner.execute_hook(el)

@pytest.mark.asyncio
@pytest.mark.parametrize("filepath, full_data, test_data", get_test_cases())
async def test_execute_dsl_scenario(dt_adapter, wait_dt, pytestconfig, filepath, full_data, test_data):
    __tracebackhide__ = True
    runner = DslRunner(dt_adapter, full_data)
    
    # Run beforeEach hooks from the same file
    for el in full_data.get("elements", []):
        if el["type"] == "LifecycleHook" and el.get("hookType") == "beforeEach":
            await runner.execute_hook(el)
            
    # Run the test definition
    verbose = pytestconfig.getoption("--monitor")
    try:
        await runner.execute_test(test_data, wait_dt, verbose=verbose)
    except MetamorphicRelationError as e:
        pytest.fail(str(e), pytrace=False)
    
    # Run afterEach hooks from the same file
    for el in full_data.get("elements", []):
        if el["type"] == "LifecycleHook" and el.get("hookType") == "afterEach":
            await runner.execute_hook(el)

@pytest.mark.asyncio
async def test_dsl_hooks_after_all(dt_adapter):
    """Executes AfterAll hooks."""
    runner = DslRunner(dt_adapter, {})
    for filepath in TEST_JSONS:
        if not os.path.exists(filepath): continue
        with open(filepath, "r") as f:
            data = json.load(f)
        for el in data.get("elements", []):
            if el["type"] == "LifecycleHook" and el.get("hookType") == "afterAll":
                await runner.execute_hook(el)
