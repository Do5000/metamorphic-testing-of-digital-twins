import pytest
import asyncio

@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_failing_sensor_monotony(dt_adapter, live_monitor, wait_dt):
    actuator = "light.norden_fenster"
    actuator_feature = "brightness"
    sensor = "Illuminance.Room518a_Window"
    sensor_feature = "Illuminance"
    
    # --- Source Test Case ---
    # Wir schalten das Licht aus (0 Helligkeit)
    await dt_adapter.set_feature_value(actuator, actuator_feature, 0)
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))
    
    # --- Follow-up Test Case ---
    # Wir machen das Licht an (80 Helligkeit)
    await dt_adapter.set_feature_value(actuator, actuator_feature, 80)
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))
    
    # Die Monotonie-Regel besagt: Wenn der Aktuator-Wert erhöht wird (Licht an),
    # darf der Sensor-Wert (Helligkeit) nicht sinken! (followup >= source)
    assert followup_val >= source_val, f"Monotony broken: Es wurde dunkler statt heller! {followup_val} < {source_val}"
