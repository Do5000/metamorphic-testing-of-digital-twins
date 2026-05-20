import pytest

def validate(result, **kwargs):
    __tracebackhide__ = True
    source_val, followup_val = result[0], result[1]
    
    if not (followup_val >= source_val):
        pytest.fail(f"Metamorphic Relation (Monotonicity) failed: {followup_val} is not >= {source_val}", pytrace=False)
        
    print(f"\n      [MR CHECK] Monotonicity PASSED: {followup_val} >= {source_val}")
