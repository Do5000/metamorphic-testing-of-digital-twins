import pytest
import asyncio

@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_light_sensor_monotony(dt_adapter, live_monitor, wait_dt):
    actuator = "switch.licht_schalter"
    sensor = "TSL2_Keyboard_spec.Room518a_WP1"
    sensor_feature = "TSL2_Keyboard_spec"
    
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(actuator, "state", 0)
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))
    
    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(actuator, "state", 1)
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))
    
    assert followup_val >= source_val, f"Monotony broken: {followup_val} < {source_val}"
