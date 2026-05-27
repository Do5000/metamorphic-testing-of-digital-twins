from .base import MetamorphicRelation, MetamorphicRelationError

class ProportionalityRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", 0.0)
        
        s1, f1, s2, f2 = result

        # Both sensors unchanged → trivially proportional
        if s1 == f1 and s2 == f2:
            print("\n      [MR CHECK] Proportionality PASSED: Both sensors remained completely unchanged (0% change)")
            return

        # One sensor unchanged while the other changed → not proportional
        if s1 == f1 or s2 == f2:
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Proportionality) failed: One sensor changed, the other did not "
                f"(sensor1: {s1} -> {f1}, sensor2: {s2} -> {f2})"
            )

        # Guard against zero baselines (cannot compute percentage change)
        if s1 == 0 or s2 == 0:
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Proportionality) failed: Baseline value is 0, "
                f"cannot compute percentage change (sensor1: {s1}, sensor2: {s2})"
            )

        # Calculate percentage change for each sensor
        pct_change1 = abs(f1 - s1) / abs(s1)
        pct_change2 = abs(f2 - s2) / abs(s2)

        # Absolute difference between the two percentage changes
        pct_deviation = abs(pct_change1 - pct_change2)

        if pct_deviation > tolerance:
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Proportionality) failed: "
                f"Percentage changes deviate by {pct_deviation * 100:.2f}% which exceeds tolerance of {tolerance * 100:.1f}% "
                f"(sensor1: {pct_change1 * 100:.2f}%, sensor2: {pct_change2 * 100:.2f}%)"
            )

        print(
            f"\n      [MR CHECK] Proportionality PASSED: "
            f"Percentage changes deviate by {pct_deviation * 100:.2f}% which is within tolerance of {tolerance * 100:.1f}% "
            f"(sensor1: {pct_change1 * 100:.2f}%, sensor2: {pct_change2 * 100:.2f}%)"
        )
