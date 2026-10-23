from .base import MetamorphicRelation, MetamorphicRelationError
from .. import config

class ConservationRelation(MetamorphicRelation):
    def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        tolerance = self.kwargs.get("tolerance", config.DEFAULT_RELATION_TOLERANCE)

        if not result or len(result) < 2:
            raise MetamorphicRelationError(
                f"Conservation relation requires at least one source and one follow-up sensor reading (got: {result})"
            )

        # Support both tuple/list of sensor lists ([s0, s1], [f0, f1]) and interleaved runner format [s0, f0, s1, f1, ...]
        if len(result) == 2 and isinstance(result[0], (list, tuple)) and isinstance(result[1], (list, tuple)):
            source_vals = list(result[0])
            followup_vals = list(result[1])
        elif isinstance(result, dict) and "source" in result and "followup" in result:
            source_vals = result["source"] if isinstance(result["source"], (list, tuple)) else [result["source"]]
            followup_vals = result["followup"] if isinstance(result["followup"], (list, tuple)) else [result["followup"]]
        else:
            # Runner passes interleaved [s0, f0, s1, f1, ...] or simple pair [s0, f0]
            source_vals = list(result[0::2])
            followup_vals = list(result[1::2])

        if len(source_vals) != len(followup_vals):
            raise MetamorphicRelationError(
                f"Conservation check failed: Mismatched number of source readings ({len(source_vals)}) and follow-up readings ({len(followup_vals)})"
            )

        if any(v is None for v in source_vals) or any(v is None for v in followup_vals):
            raise AssertionError(
                f"Conservation check failed: Sensor value is None (source: {source_vals}, follow-up: {followup_vals})"
            )

        try:
            source_floats = [float(v) for v in source_vals]
            followup_floats = [float(v) for v in followup_vals]
        except (TypeError, ValueError):
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Conservation) failed: Non-numeric values found (source: {source_vals}, follow-up: {followup_vals})"
            )

        sum_source = sum(source_floats)
        sum_followup = sum(followup_floats)

        # Paper formula: |sum(O_f) - sum(O_s)| <= eps_tau(sum(O_s), sum(O_f))
        # where eps_tau(A, B) = tau * max(|A|, |B|, 1.0)
        diff = abs(sum_followup - sum_source)
        max_val = max(abs(sum_source), abs(sum_followup), 1.0)
        allowed = tolerance if tolerance > 1.0 else max_val * tolerance

        sensor_desc = f"{len(source_floats)} sensor(s)"
        if diff > allowed:
            raise MetamorphicRelationError(
                f"Metamorphic Relation (Conservation) failed for {sensor_desc}: aggregate followup {sum_followup:.4f} vs aggregate source {sum_source:.4f} "
                f"(diff {diff:.4f} > allowed {allowed:.4f}, tolerance: {tolerance})"
            )

        if len(source_floats) == 1:
            print(f"\n      [MR CHECK] Conservation PASSED: {sum_followup:.4f} approx {sum_source:.4f} (diff {diff:.4f} <= {allowed:.4f})")
        else:
            print(f"\n      [MR CHECK] Conservation PASSED ({sensor_desc}): aggregate followup {sum_followup:.4f} approx aggregate source {sum_source:.4f} (diff {diff:.4f} <= {allowed:.4f})")

