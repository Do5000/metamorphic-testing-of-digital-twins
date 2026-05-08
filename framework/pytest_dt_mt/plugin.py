import pytest
import asyncio
import functools
import inspect
import os
import datetime
import json

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

def _load_json_profile(file_path):
    """Internal helper to load reference tables with robust path resolution."""
    if os.path.exists(file_path):
        full_path = file_path
    else:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        framework_dir = os.path.dirname(plugin_dir)
        full_path = os.path.join(framework_dir, file_path)

    if not os.path.exists(full_path):
        return None
    try:
        with open(full_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def validate_mr_result(result, **kwargs):
    __tracebackhide__ = True
    if result is None or not isinstance(result, (tuple, list)) or len(result) < 2:
        return

    mr_type = kwargs.get("type")
    tolerance = kwargs.get("tolerance", 0.0)
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

    elif mr_type == "proportionality":
        if len(result) < 4:
            return # Requires 4 values: (source_main, followup_main, source_ref, followup_ref)
            
        s1, f1 = float(result[0]), float(result[1])
        s2, f2 = float(result[2]), float(result[3])
        
        # Proportionality check: f1/s1 approx f2/s2
        # Cross-multiply to avoid division by zero: f1 * s2 approx f2 * s1
        diff = abs(f1 * s2 - f2 * s1)
        norm = max(abs(s1 * s2), 1.0)
        rel_diff = diff / norm
        
        if rel_diff > tolerance:
            pytest.fail(f"Metamorphic Relation (Proportionality) failed: Sensor A ({s1}->{f1}) and Sensor B ({s2}->{f2}) inconsistent (rel_diff {rel_diff:.3f} > allowed {tolerance})", pytrace=False)
        print(f"\n      [MR CHECK] Proportionality PASSED: Sensors A and B show consistent relative change (rel_diff {rel_diff:.3f} <= {tolerance})")

    elif mr_type == "substitution":
        # Expects result = (current_new_val, current_neighbor_val)
        new_val, neighbor_val = float(result[0]), float(result[1])
        
        profile_path = kwargs.get("profile", "sensor_profile.json")
        profile = _load_json_profile(profile_path)
        
        if profile is None:
            pytest.fail(f"Metamorphic Relation (Substitution) failed: Reference profile '{profile_path}' not found or invalid.", pytrace=False)
            
        # Find best match in table based on neighbor sensor
        try:
            best_match = min(profile, key=lambda x: abs(x["neighbor_sensor"] - neighbor_val))
            historic_old_val = best_match["old_sensor"]
            match_ref_val = best_match["neighbor_sensor"]
        except (KeyError, TypeError):
            pytest.fail(f"Metamorphic Relation (Substitution) failed: Profile format invalid (missing 'neighbor_sensor' or 'old_sensor').", pytrace=False)

        diff = abs(new_val - historic_old_val)
        max_val = max(abs(historic_old_val), abs(new_val), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance
        
        if diff > allowed:
            pytest.fail(f"Metamorphic Relation (Substitution) failed: New sensor {new_val} vs Historical old sensor {historic_old_val} (Matched by neighbor {neighbor_val} approx {match_ref_val} | diff {diff} > allowed {allowed})", pytrace=False)
        
        print(f"\n      [MR CHECK] Substitution PASSED: New sensor {new_val} matches Historical entry {historic_old_val} (Neighbor match: {neighbor_val} approx {match_ref_val})")


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
