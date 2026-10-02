from .base import MetamorphicRelation, MetamorphicRelationError

class InvarianceRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", 0.0)
        source_val = result[0]
        followup_val = result[1]
        intermediate_val = result[2] if len(result) > 2 else None
        
        try:
            cmp_source = float(source_val)
            cmp_followup = float(followup_val)
        except (TypeError, ValueError):
            # Fallback if values cannot be cast to float.
            if source_val == followup_val:
                if intermediate_val is not None and intermediate_val == source_val:
                    raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: Intermediate state did not change from source ({source_val})")
                print(f"\n      [MR CHECK] Invariance PASSED (Exact Match): {followup_val} == {source_val}")
                return
            else:
                raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: {followup_val} != {source_val} (non-numeric)")
        
        diff = abs(cmp_followup - cmp_source)
        max_val = max(abs(cmp_source), abs(cmp_followup), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance
        
        if diff > allowed:
            raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: {cmp_followup} vs {cmp_source} (diff {diff} > allowed {allowed})")
            
        if intermediate_val is not None:
            try:
                cmp_intermediate = float(intermediate_val)
                diff_inter = abs(cmp_source - cmp_intermediate)
                if diff_inter <= allowed:
                    raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: Intermediate state {cmp_intermediate} did not change significantly from source {cmp_source} (diff {diff_inter} <= allowed {allowed})")
            except (TypeError, ValueError):
                if intermediate_val == source_val:
                    raise MetamorphicRelationError(f"Metamorphic Relation (Invariance) failed: Intermediate state did not change from source ({source_val})")
            
        print(f"\n      [MR CHECK] Invariance PASSED: {followup_val} approx {source_val} (diff {diff} <= {allowed})")
