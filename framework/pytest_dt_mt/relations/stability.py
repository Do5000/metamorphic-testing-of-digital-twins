import asyncio
from .base import MetamorphicRelation, MetamorphicRelationError
from pytest_dt_mt.core import LiveValueMonitor

class StabilityRelation(MetamorphicRelation):
    async def evaluate(self, result, dt_adapter=None):
        __tracebackhide__ = True
        
        if dt_adapter is None:
            raise MetamorphicRelationError("dt_adapter is required for Stability relation")
        if not result or len(result) < 1:
            raise MetamorphicRelationError("Stability relation requires the test to return at least a 'sensor_id'")
            
        sensor_id = result[0]
        feature_name = result[1] if len(result) > 1 else self.kwargs.get("feature", "state")
        
        duration = self.kwargs.get("duration", 10.0)
        tolerance = self.kwargs.get("tolerance", 0.0)
        verbose = self.kwargs.get("verbose", False)
            
        print(f"\n      [MR CHECK] Stability: Monitoring '{sensor_id}' ({feature_name}) for {duration}s (allowed fluctuation tolerance: {tolerance})...")
        
        monitor = LiveValueMonitor(dt_adapter, sensor_id, feature_name, interval=0.5, verbose=verbose)
        async with monitor:
            await asyncio.sleep(duration)
            
        vals = [v for (_, v) in monitor.history if v is not None]
        if not vals:
            raise MetamorphicRelationError(f"Stability check failed: No valid data points received from '{sensor_id}' in {duration}s")
            
        # Optional: verify if all values are numeric. If not, just check exact equality
        all_numeric = all(isinstance(v, (int, float)) for v in vals)
        
        if all_numeric:
            max_v = max(vals)
            min_v = min(vals)
            diff = abs(max_v - min_v)
            
            allowed = tolerance if tolerance > 1.0 else max(abs(max_v), abs(min_v), 1.0) * tolerance
            
            if diff > allowed:
                raise MetamorphicRelationError(f"Metamorphic Relation (Stability) failed: Fluctuation {diff:.3f} > allowed {allowed:.3f} (Max: {max_v}, Min: {min_v}) over {duration}s")
                
            print(f"      [MR CHECK] Stability PASSED: Fluctuation diff {diff:.3f} <= allowed tolerance {tolerance*100}% [= {allowed:.3f}] (Max: {max_v}, Min: {min_v}) over {duration}s")
        else:
            first_v = vals[0]
            if any(v != first_v for v in vals):
                raise MetamorphicRelationError(f"Metamorphic Relation (Stability) failed: Value changed during monitoring period")
            print(f"      [MR CHECK] Stability PASSED: Value remained '{first_v}' for {duration}s")
