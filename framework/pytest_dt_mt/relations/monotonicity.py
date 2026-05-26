from .base import MetamorphicRelation, MetamorphicRelationError

class MonotonicityRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        source_val, followup_val = result[0], result[1]
        
        if not (followup_val >= source_val):
            raise MetamorphicRelationError(f"Metamorphic Relation (Monotonicity) failed: {followup_val} is not >= {source_val}")
            
        print(f"\n      [MR CHECK] Monotonicity PASSED: {followup_val} >= {source_val}")
