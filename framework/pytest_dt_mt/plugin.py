import pytest
import asyncio
import functools
import inspect
import os
import datetime
import json

from pytest_dt_mt.relations.monotonicity import MonotonicityRelation
from pytest_dt_mt.relations.invariance import InvarianceRelation
from pytest_dt_mt.relations.conservation import ConservationRelation
from pytest_dt_mt.relations.proportionality import ProportionalityRelation
from pytest_dt_mt.relations.substitution import SubstitutionRelation
from pytest_dt_mt.relations.stability import StabilityRelation
from pytest_dt_mt.relations.base import MetamorphicRelationError

def pytest_addoption(parser):
    parser.addoption("--wait-time", action="store", default=30.0, type=float, help="Global wait time in seconds for physical simulation")
    parser.addoption("--monitor", action="store_true", help="Enable live printing of sensor values during tests")
    parser.addoption("--log", action="store_true", help="Enable detailed logging into a session-based folder")

def pytest_configure(config):
    """
    Register custom markers for Metamorphic Testing.
    """
    config.addinivalue_line(
        "markers", "mr(type, tolerance): mark test as a Metamorphic Relation test"
    )

def pytest_collection_modifyitems(items):
    """
    Wrap test functions marked with @pytest.mark.mr to automatically
    validate their return values.
    """
    for item in items:
        marker = item.get_closest_marker("mr")
        if marker:
            item.obj = wrap_mr_test(item.obj, marker)

def wrap_mr_test(original_obj, marker):
    if inspect.iscoroutinefunction(original_obj):
        @functools.wraps(original_obj)
        async def wrapped_test(*args, **kwargs):
            __tracebackhide__ = True
            result = await original_obj(*args, **kwargs)
            
            # Find dt_adapter
            dt_adapter = None
            for arg in args:
                if hasattr(arg, "get_feature_value"):
                    dt_adapter = arg
                    break
            if not dt_adapter:
                for k, v in kwargs.items():
                    if hasattr(v, "get_feature_value"):
                        dt_adapter = v
                        break
                        
            await validate_mr_result(result, dt_adapter=dt_adapter, **marker.kwargs)
            return result
        return wrapped_test
    else:
        @functools.wraps(original_obj)
        def wrapped_test(*args, **kwargs):
            __tracebackhide__ = True
            result = original_obj(*args, **kwargs)
            
            # Find dt_adapter
            dt_adapter = None
            for arg in args:
                if hasattr(arg, "get_feature_value"):
                    dt_adapter = arg
                    break
            if not dt_adapter:
                for k, v in kwargs.items():
                    if hasattr(v, "get_feature_value"):
                        dt_adapter = v
                        break
                        
            # Run the async validator synchronously in fallback
            loop = asyncio.get_event_loop()
            loop.run_until_complete(validate_mr_result(result, dt_adapter=dt_adapter, **marker.kwargs))
            return result
        return wrapped_test

async def validate_mr_result(result, dt_adapter=None, **kwargs):
    __tracebackhide__ = True
    mr_type = kwargs.get("type")
    
    relation = None
    
    if mr_type == "stability":
        relation = StabilityRelation(**kwargs)
    elif mr_type == "monotonicity":
        relation = MonotonicityRelation(**kwargs)
    elif mr_type == "invariance":
        relation = InvarianceRelation(**kwargs)
    elif mr_type == "conservation":
        relation = ConservationRelation(**kwargs)
    elif mr_type == "proportionality":
        relation = ProportionalityRelation(**kwargs)
    elif mr_type == "substitution":
        relation = SubstitutionRelation(**kwargs)

    if relation:
        try:
            if inspect.iscoroutinefunction(relation.evaluate):
                await relation.evaluate(result, dt_adapter=dt_adapter)
            else:
                relation.evaluate(result, dt_adapter=dt_adapter)
        except MetamorphicRelationError as e:
            pytest.fail(str(e), pytrace=False)

def pytest_runtest_makereport(item, call):
    """
    Custom reporting hook. Can be used to inject additional MT-specific output.
    """
    pass

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Creates a single structured log file for the entire test session if --log is enabled.
    Also prints the measured latencies for each module clearly to the console.
    """
    from pytest_dt_mt.fixtures import _MODULE_WAIT_DT
    
    if _MODULE_WAIT_DT:
        terminalreporter.write_sep("=", "LATENCY CALIBRATION SUMMARY", bold=True, yellow=True)
        for module_name, latency in _MODULE_WAIT_DT.items():
            if latency is not None:
                terminalreporter.write_line(f"  - Module '{module_name}': {latency:.3f}s")
            else:
                terminalreporter.write_line(f"  - Module '{module_name}': Default wait time")
        terminalreporter.write_line("")

    if not config.getoption("--log"):
        return

    # Create base directory
    log_dir = "test_reports"
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print(f"\n[ERROR] Could not create log directory {log_dir}: {e}")
        return

    # Create a unique filename for the session
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(log_dir, f"report_{timestamp}.log")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{'='*80}\n")
        f.write(f" METAMORPHIC TESTING SESSION REPORT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*80}\n\n")
        
        # Process all outcomes
        for outcome in ["passed", "failed", "error"]:
            reports = terminalreporter.stats.get(outcome, [])
            for rep in reports:
                f.write(f"[{outcome.upper()}] {rep.nodeid}\n")
                
                if rep.capstdout:
                    f.write("--- Captured Output ---\n")
                    f.write(rep.capstdout)
                    f.write("\n")
                
                if outcome != "passed":
                    f.write("--- Error Details ---\n")
                    f.write(str(rep.longrepr))
                    f.write("\n")
                
                f.write("-" * 80 + "\n")

        # Session Summary
        passed = len(terminalreporter.stats.get('passed', []))
        failed = len(terminalreporter.stats.get('failed', []))
        f.write(f"\nTOTAL RESULT: {passed} PASSED, {failed} FAILED\n")
        
        if _MODULE_WAIT_DT:
            f.write(f"\n{'='*80}\n")
            f.write(f" LATENCY CALIBRATION SUMMARY\n")
            f.write(f"{'='*80}\n")
            for module_name, latency in _MODULE_WAIT_DT.items():
                if latency is not None:
                    f.write(f"  - Module '{module_name}': {latency:.3f}s\n")
                else:
                    f.write(f"  - Module '{module_name}': Default wait time\n")
            f.write("\n")

    print(f"\n[INFO] Session report created: {file_path}")
