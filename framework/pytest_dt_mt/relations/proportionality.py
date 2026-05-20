import pytest

def validate(result, **kwargs):
    __tracebackhide__ = True
    if len(result) < 4:
        return  # Requires 4 values: (source_main, followup_main, source_ref, followup_ref)
        
    tolerance = kwargs.get("tolerance", 0.0)
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
