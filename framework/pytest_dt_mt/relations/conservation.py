import pytest

def validate(result, **kwargs):
    __tracebackhide__ = True
    tolerance = kwargs.get("tolerance", 0.0)
    source_val, followup_val = result[0], result[1]
    
    diff = abs(followup_val - source_val)
    max_val = max(abs(source_val), abs(followup_val), 1.0)
    allowed = tolerance if tolerance > 1.0 else max_val * tolerance
    
    if diff > allowed:
        pytest.fail(f"Metamorphic Relation (Conservation) failed: {followup_val} vs {source_val} (diff {diff} > allowed {allowed})", pytrace=False)
        
    print(f"\n      [MR CHECK] Conservation PASSED: {followup_val} approx {source_val} (diff {diff} <= {allowed})")
