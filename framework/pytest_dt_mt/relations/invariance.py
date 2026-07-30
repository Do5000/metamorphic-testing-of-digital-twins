from .base import MetamorphicRelation, MetamorphicRelationError

class InvarianceRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", 0.0)
        source_val, followup_val = result[0], result[1]
        try:
            cmp_source = float(source_val)
            cmp_followup = float(followup_val)
        except (TypeError, ValueError):
            # Fallback if values cannot be cast to float. Will likely fail in abs/subtraction, 
            # but handles case where they might be equal strings.
            if source_val == followup_val:
                print(f"\n      [MR CHECK] Invariance PASSED (Exact Match): {followup_val} == {source_val}")
                return
            else:
                raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: {followup_val} != {source_val} (non-numeric)")
        
        diff = abs(cmp_followup - cmp_source)
        max_val = max(abs(cmp_source), abs(cmp_followup), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance
        
        if diff > allowed:
            raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: {cmp_followup} vs {cmp_source} (diff {diff} > allowed {allowed})")
            
        print(f"\n      [MR CHECK] Invariance PASSED: {followup_val} approx {source_val} (diff {diff} <= {allowed})")
