import asyncio
import pytest

async def validate(result, dt_adapter=None, **kwargs):
    __tracebackhide__ = True
    if dt_adapter is None:
        pytest.fail("Metamorphic Relation (Stability) failed: dt_adapter is not available to measure sensor.", pytrace=False)

    if isinstance(result, tuple) and len(result) >= 1:
        sensor = result[0]
        sensor_feature = result[1] if len(result) >= 2 else kwargs.get("sensor_feature", "state")
    elif isinstance(result, str):
        sensor = result
        sensor_feature = kwargs.get("sensor_feature", "state")
    else:
        sensor = kwargs.get("sensor")
        sensor_feature = kwargs.get("sensor_feature", "state")

    tolerance = kwargs.get("tolerance")
    duration = kwargs.get("duration", 5.0)
    
    if not sensor:
        pytest.fail("Metamorphic Relation (Stability) failed: 'sensor' argument is required.", pytrace=False)
    if tolerance is None:
        pytest.fail("Metamorphic Relation (Stability) failed: 'tolerance' argument is required.", pytrace=False)
        
    print(f"\n      [MR CHECK] Stability: Monitoring '{sensor}' ({sensor_feature}) for {duration}s (allowed fluctuation tolerance: {tolerance})...")
    
    values = []
    start_time = asyncio.get_event_loop().time()
    
    # Poll the sensor for the specified duration
    while asyncio.get_event_loop().time() - start_time < duration:
        val = await dt_adapter.get_feature_value(sensor, sensor_feature, silent=True)
        if val is not None:
            try:
                values.append(float(val))
            except (ValueError, TypeError):
                pass
        await asyncio.sleep(0.2)
        
    if not values:
        pytest.fail(f"Metamorphic Relation (Stability) failed: No numeric values could be read from sensor '{sensor}' during {duration}s.", pytrace=False)
        
    avg_val = sum(values) / len(values)
    ref_val = max(abs(avg_val), 1.0)
    
    # If tolerance is <= 1.0, treat it as a percentage/fraction of the reference value
    is_percent = tolerance <= 1.0
    allowed = tolerance if not is_percent else ref_val * tolerance
    tolerance_str = f"{tolerance * 100:.1f}%" if is_percent else f"{tolerance}"
    
    min_val = min(values)
    max_val = max(values)
    diff = max_val - min_val
    
    if diff > allowed:
        pytest.fail(f"Metamorphic Relation (Stability) failed: Sensor '{sensor}' fluctuated too much! Max value: {max_val}, Min value: {min_val} (diff {diff:.3f} > allowed tolerance {tolerance_str} [= {allowed:.3f}])", pytrace=False)
        
    print(f"      [MR CHECK] Stability PASSED: Fluctuation diff {diff:.3f} <= allowed tolerance {tolerance_str} [= {allowed:.3f}] (Max: {max_val}, Min: {min_val}) over {duration}s")
