import pytest
import asyncio

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "off")


async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose ", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")

@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_light_sensor_monotony(dt_adapter, live_monitor, wait_dt):
    # Arrange
    actuator = "light.schreibtisch_lampe"
    sensor = "sensor.arbeitsplatz_helligkeit"
    sensor_feature = "state"


    # Act
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(actuator, "state", "off")
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))
    
    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(actuator, "state", "on")
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))

    # Assert
    return source_val, followup_val


async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.steckdose_ecke_fernseher", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")