from .base import MetamorphicRelation, MetamorphicRelationError
from .. import config

class ProportionalityRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", config.DEFAULT_RELATION_TOLERANCE)

        if not result or len(result) < 4:
            raise MetamorphicRelationError(
                f"Proportionality relation requires at least 2 sensors (got: {result})"
            )

        # Support both tuple/list of sensor lists ([s0, s1, ...], [f0, f1, ...])
        # and interleaved runner format [s0, f0, s1, f1, ...]
        if len(result) == 2 and isinstance(result[0], (list, tuple)) and isinstance(result[1], (list, tuple)):
            source_vals = list(result[0])
            followup_vals = list(result[1])
        elif isinstance(result, dict) and "source" in result and "followup" in result:
            source_vals = result["source"] if isinstance(result["source"], (list, tuple)) else [result["source"]]
            followup_vals = result["followup"] if isinstance(result["followup"], (list, tuple)) else [result["followup"]]
        else:
            source_vals = list(result[0::2])
            followup_vals = list(result[1::2])

        if len(source_vals) < 2 or len(source_vals) != len(followup_vals):
            raise MetamorphicRelationError(
                f"Proportionality check failed: Requires at least 2 sensor pairs with equal length "
                f"(source: {len(source_vals)}, follow-up: {len(followup_vals)})"
            )

        # 1. Null-value check
        if any(v is None for v in source_vals) or any(v is None for v in followup_vals):
            raise AssertionError(
                f"Proportionality check failed: Sensor value is None (source: {source_vals}, follow-up: {followup_vals})"
            )

        # 2. Convert readings to float
        try:
            source_floats = [float(v) for v in source_vals]
            followup_floats = [float(v) for v in followup_vals]
        except (TypeError, ValueError):
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Proportionality) failed: Non-numeric values found "
                f"(source: {source_vals}, follow-up: {followup_vals})"
            )

        # 3. Check for trivial proportionality (all sensors remained completely unchanged)
        if all(s == f for s, f in zip(source_floats, followup_floats)):
            print("\n      [MR CHECK] Proportionality PASSED: All sensors remained completely unchanged (0% change)")
            return

        # 4. Zero-baseline guard to avoid division by zero
        for idx, s in enumerate(source_floats):
            if s == 0.0:
                raise MetamorphicRelationError(
                    f"Metamorphic Relation (Proportionality) failed: Baseline value of sensor {idx + 1} is 0.0, "
                    f"cannot compute relative change (source: {source_floats})"
                )

        # 5. Paper formula: r_j = (O_j^f - O_j^s) / O_j^s
        rel_changes = [(f - s) / s for s, f in zip(source_floats, followup_floats)]

        # 6. Pairwise check across all pairs j, k: |r_j - r_k| <= tau
        # The maximum pairwise deviation max_{j,k} |r_j - r_k| equals max(r) - min(r)
        max_r = max(rel_changes)
        min_r = min(rel_changes)
        max_idx = rel_changes.index(max_r)
        min_idx = rel_changes.index(min_r)
        max_deviation = max_r - min_r

        summary_str = ", ".join(f"S{i+1}: {r*100:+.2f}%" for i, r in enumerate(rel_changes))

        if max_deviation > tolerance:
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Proportionality) failed across {len(rel_changes)} sensors: "
                f"Maximum relative deviation is {max_deviation * 100:.2f}% which exceeds tolerance of {tolerance * 100:.1f}%. "
                f"(Widest gap between Sensor {max_idx + 1} ({max_r * 100:+.2f}%) and Sensor {min_idx + 1} ({min_r * 100:+.2f}%); "
                f"All changes: [{summary_str}])"
            )

        print(
            f"\n      [MR CHECK] Proportionality PASSED ({len(rel_changes)} sensors): "
            f"Relative changes deviate by at most {max_deviation * 100:.2f}% <= tolerance {tolerance * 100:.1f}% "
            f"([{summary_str}])"
        )

