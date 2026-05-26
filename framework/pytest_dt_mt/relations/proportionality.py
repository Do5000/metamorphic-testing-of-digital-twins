from .base import MetamorphicRelation, MetamorphicRelationError

class ProportionalityRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", 0.0)
        
        s1, f1, s2, f2 = result
        diff1 = abs(f1 - s1)
        diff2 = abs(f2 - s2)

        if diff1 == 0 and diff2 == 0:
            print("\n      [MR CHECK] Proportionality PASSED: Both sensors remained completely unchanged (0 diff)")
            return
            
        if diff1 == 0 or diff2 == 0:
            raise MetamorphicRelationError(f"Metamorphic Relation (Proportionality) failed: One sensor changed, the other did not (diffs: {diff1:.1f}, {diff2:.1f})")

        ratio = diff1 / diff2 if diff2 > diff1 else diff2 / diff1
        min_allowed_ratio = 1.0 - tolerance

        if ratio < min_allowed_ratio:
            raise MetamorphicRelationError(f"Metamorphic Relation (Proportionality) failed: Ratio {ratio:.2f} < {min_allowed_ratio:.2f} (diffs: {diff1:.1f}, {diff2:.1f})")

        print(f"\n      [MR CHECK] Proportionality PASSED: Ratio {ratio:.2f} >= {min_allowed_ratio:.2f} (diffs: {diff1:.1f}, {diff2:.1f})")
