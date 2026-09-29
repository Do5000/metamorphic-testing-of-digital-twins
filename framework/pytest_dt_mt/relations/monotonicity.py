from .base import MetamorphicRelation, MetamorphicRelationError

class MonotonicityRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", 0.0)
        source_val, followup_val = result[0], result[1]
        
        try:
            cmp_source = float(source_val)
            cmp_followup = float(followup_val)
        except (TypeError, ValueError):
            cmp_source = source_val
            cmp_followup = followup_val
            
        if isinstance(cmp_source, float) and isinstance(cmp_followup, float) and tolerance > 0.0:
            max_val = max(abs(cmp_source), abs(cmp_followup), 1.0)
            allowed = tolerance if tolerance > 1.0 else max_val * tolerance
            
            if not (cmp_followup > cmp_source + allowed):
                raise MetamorphicRelationError(f"Metamorphic Relation (Monotonicity) failed: {followup_val} is not > {source_val} + {allowed:.4f} (tolerance)")
                
            print(f"\n      [MR CHECK] Monotonicity PASSED: {followup_val} > {source_val} + {allowed:.4f} (tolerance)")
        else:
            if not (cmp_followup >= cmp_source):
                raise MetamorphicRelationError(f"Metamorphic Relation (Monotonicity) failed: {followup_val} is not >= {source_val}")
                
            print(f"\n      [MR CHECK] Monotonicity PASSED: {followup_val} >= {source_val}")

