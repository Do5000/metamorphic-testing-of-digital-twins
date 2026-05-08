import pytest
import asyncio
import functools
import inspect

def pytest_addoption(parser):
    parser.addoption("--wait-time", action="store", default=30.0, type=float, help="Global wait time in seconds for physical simulation")
    parser.addoption("--monitor", action="store_true", help="Enable live printing of sensor values during tests")

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
    mr_type = marker.kwargs.get("type")
    tolerance = marker.kwargs.get("tolerance", 0.0)

    if inspect.iscoroutinefunction(original_obj):
        @functools.wraps(original_obj)
        async def wrapped_test(*args, **kwargs):
            __tracebackhide__ = True
            result = await original_obj(*args, **kwargs)
            validate_mr_result(result, mr_type, tolerance)
            return result
        return wrapped_test
    else:
        @functools.wraps(original_obj)
        def wrapped_test(*args, **kwargs):
            __tracebackhide__ = True
            result = original_obj(*args, **kwargs)
            validate_mr_result(result, mr_type, tolerance)
            return result
        return wrapped_test

def validate_mr_result(result, mr_type, tolerance):
    __tracebackhide__ = True
    if result is None or not isinstance(result, (tuple, list)) or len(result) < 2:
        return

    source_val, followup_val = result[0], result[1]

    if mr_type == "monotonicity":
        if not (followup_val >= source_val):
            pytest.fail(f"Metamorphic Relation (Monotonicity) failed: {followup_val} is not >= {source_val}", pytrace=False)
        print(f"\n      [MR CHECK] Monotonicity PASSED: {followup_val} >= {source_val}")
        
    elif mr_type == "invariance":
        diff = abs(followup_val - source_val)
        max_val = max(abs(source_val), abs(followup_val), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance
        
        if diff > allowed:
            pytest.fail(f"Metamorphic Relation (Invariance) failed: {followup_val} vs {source_val} (diff {diff} > allowed {allowed})", pytrace=False)
        print(f"\n      [MR CHECK] Invariance PASSED: {followup_val} approx {source_val} (diff {diff} <= {allowed})")

    elif mr_type == "conservation":
        diff = abs(followup_val - source_val)
        max_val = max(abs(source_val), abs(followup_val), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance
        
        if diff > allowed:
            pytest.fail(f"Metamorphic Relation (Conservation) failed: {followup_val} vs {source_val} (diff {diff} > allowed {allowed})", pytrace=False)
        print(f"\n      [MR CHECK] Conservation PASSED: {followup_val} approx {source_val} (diff {diff} <= {allowed})")


def pytest_runtest_makereport(item, call):
    """
    Custom reporting hook. Can be used to inject additional MT-specific output.
    """
    pass
