import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "off")
    
    # Auto-calibrate wait time using the monotony relation workflow
    await dt_adapter.measure_latency(
        actuator="light.schreibtisch_lampe",
        actuatorFeature="state",
        valOff="off",
        valOn="on",
        sensor="sensor.esp_c3_helligkeit",
        sensorFeature="state",
        minChangePercent=0.10,
        toleranceFactor = 1.1,
        addSeconds = 0,
        timeout = 3.0,
        runs = 2

    )


async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_monotony(dt_adapter, live_monitor, wait_dt):
    # Arrange
    actuator = "light.schreibtisch_lampe"
    actuatorFeature = "state"

    sensor = "sensor.esp_c3_helligkeit"
    sensorFeature = "state"

    # Act
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(actuator, actuatorFeature, "off")
    async with live_monitor(sensor, sensorFeature):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(sensor, sensorFeature))

    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(actuator, actuatorFeature, "on")
    async with live_monitor(sensor, sensorFeature):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(sensor, sensorFeature))

    # Assert
    return source_val, followup_val


async def afterAll(dt_adapter, wait_dt):
    print("\n[HOOK] afterAll: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")

    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "on")
