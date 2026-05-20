import pytest
import asyncio
import functools
import inspect
import os
import datetime
import json

from pytest_dt_mt.relations import monotonicity
from pytest_dt_mt.relations import invariance
from pytest_dt_mt.relations import conservation
from pytest_dt_mt.relations import proportionality
from pytest_dt_mt.relations import substitution

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
            validate_mr_result(result, **marker.kwargs)
            return result
        return wrapped_test
    else:
        @functools.wraps(original_obj)
        def wrapped_test(*args, **kwargs):
            __tracebackhide__ = True
            result = original_obj(*args, **kwargs)
            validate_mr_result(result, **marker.kwargs)
            return result
        return wrapped_test

def validate_mr_result(result, **kwargs):
    __tracebackhide__ = True
    if result is None or not isinstance(result, (tuple, list)) or len(result) < 2:
        return

    mr_type = kwargs.get("type")
    
    if mr_type == "monotonicity":
        monotonicity.validate(result, **kwargs)
    elif mr_type == "invariance":
        invariance.validate(result, **kwargs)
    elif mr_type == "conservation":
        conservation.validate(result, **kwargs)
    elif mr_type == "proportionality":
        proportionality.validate(result, **kwargs)
    elif mr_type == "substitution":
        substitution.validate(result, **kwargs)

def pytest_runtest_makereport(item, call):
    """
    Custom reporting hook. Can be used to inject additional MT-specific output.
    """
    pass

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Creates a single structured log file for the entire test session if --log is enabled.
    """
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

    print(f"\n[INFO] Session report created: {file_path}")
