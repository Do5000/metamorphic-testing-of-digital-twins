import asyncio
from .base import MetamorphicRelation, MetamorphicRelationError
from pytest_dt_mt.monitoring import LiveValueMonitor
from .. import config

class StabilityRelation(MetamorphicRelation):
    async def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        
        if dt_adapter is None:
            raise MetamorphicRelationError("dt_adapter is required for Stability relation")
        if not result or len(result) < 1:
            raise MetamorphicRelationError("Stability relation requires the test to return at least a 'sensor_id'")
            
        sensor_id = result[0]
        feature_name = result[1] if len(result) > 1 else self.kwargs.get("feature", "state")
        
        duration = self.kwargs.get("duration", config.DEFAULT_STABILITY_DURATION)
        tolerance = self.kwargs.get("tolerance", config.DEFAULT_RELATION_TOLERANCE)
        verbose = self.kwargs.get("verbose", False)
            
        print(f"\n      [MR CHECK] Stability: Monitoring '{sensor_id}' ({feature_name}) for {duration}s (allowed fluctuation tolerance: {tolerance})...")
        
        monitor = LiveValueMonitor(dt_adapter, sensor_id, feature_name, interval=config.DEFAULT_MONITOR_INTERVAL, verbose=verbose)
        async with monitor:
            await asyncio.sleep(duration)
            
        vals = [v for (_, v) in monitor.history if v is not None]
        if not vals:
            raise MetamorphicRelationError(f"Stability check failed: No valid data points received from '{sensor_id}' in {duration}s")
            
        # Try to parse all values as floats (since JSON/APIs often return numbers as strings like "586.67")
        parsed_vals = []
        all_numeric = True
        for v in vals:
            if isinstance(v, (int, float)):
                parsed_vals.append(v)
            else:
                try:
                    parsed_vals.append(float(v))
                except (ValueError, TypeError):
                    all_numeric = False
                    break
        
        if all_numeric:
            vals = parsed_vals  # Use the actual numbers for math
            max_v = max(vals)
            min_v = min(vals)
            diff = abs(max_v - min_v)
            
            allowed = tolerance if tolerance > 1.0 else max(abs(max_v), abs(min_v), 1.0) * tolerance
            
            if diff > allowed:
                raise MetamorphicRelationError(f"Metamorphic Relation (Stability) failed: Fluctuation {diff:.3f} > allowed {allowed:.3f} (Max: {max_v}, Min: {min_v}) over {duration}s")
                
            print(f"      [MR CHECK] Stability PASSED: Fluctuation diff {diff:.3f} <= allowed tolerance {tolerance*100}% [= {allowed:.3f}] (Max: {max_v}, Min: {min_v}) over {duration}s")
        else:
            first_v = vals[0]
            changed_v = None
            changed_idx = -1
            for i, v in enumerate(vals):
                if v != first_v:
                    changed_v = v
                    changed_idx = i
                    break
                    
            if changed_v is not None:
                raise MetamorphicRelationError(f"Metamorphic Relation (Stability) failed: Value changed during monitoring period. Expected '{first_v}' but got '{changed_v}' at index {changed_idx}.")
            print(f"      [MR CHECK] Stability PASSED: Value remained '{first_v}' for {duration}s")
