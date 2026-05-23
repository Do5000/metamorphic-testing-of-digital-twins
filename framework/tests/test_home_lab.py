import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")

    # Pre-Condition: Tests only make sense if the sun is down
    await dt_adapter.require_precondition("automation.nach_sonnenuntergang", "state", "on",skip_message="Tests require the sun to be below the horizon.")

    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "off")
    
    await dt_adapter.measure_latency(
        actuator="light.schreibtisch_lampe",
        actuator_feature="state",
        val_off="off",
        val_on="on",
        sensor="sensor.esp_c3_helligkeit",
        sensor_feature="state",
        min_change_percent=0.2,
        tolerance_factor = 1.1,
        add_seconds = 0,
        timeout = 3.0,
        runs = 5
    )

    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

    await dt_adapter.measure_latency(
        actuator="light.amelie_lampe",
        actuator_feature="state",
        val_off="off",
        val_on="on",
        sensor="sensor.esp_c3_helligkeit",
        sensor_feature="state",
        min_change_percent=0.10,
        tolerance_factor = 1.1,
        add_seconds = 0,
        timeout = 3.0,
        runs = 5
    )


async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")
    await dt_adapter.set_feature_value("light.amelie_lampe", "state", "off")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")


@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_home_monotony(dt_adapter, live_monitor, wait_dt):
    # Arrange
    actuator = "light.schreibtisch_lampe"
    actuator_feature = "state"

    sensor = "sensor.esp_c3_helligkeit"
    sensor_feature = "state"

    # Act
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(actuator, actuator_feature, "off")
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))

    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(actuator, actuator_feature, "on")
    async with live_monitor(sensor, sensor_feature):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(sensor, sensor_feature))

    # Assert
    return source_val, followup_val


@pytest.mark.asyncio
@pytest.mark.mr(type="invariance", tolerance=0.05)
async def test_home_invariance(dt_adapter, live_monitor, wait_dt):
    # Arrange
    a_id, a_feat = "light.schreibtisch_lampe", "state"
    s_id, s_feat = "sensor.esp_c3_helligkeit", "state"

    # Act
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(a_id, a_feat, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    source_val = float(await dt_adapter.get_feature_value(s_id, s_feat))

    # Reset
    await dt_adapter.set_feature_value(a_id, a_feat, "off")
    async with live_monitor(s_id, s_feat):
        await wait_dt()

    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(a_id, a_feat, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    followup_val = float(await dt_adapter.get_feature_value(s_id, s_feat))

    # Assert
    return source_val, followup_val


@pytest.mark.asyncio
@pytest.mark.mr(type="conservation", tolerance=0.05)
async def test_home_conservation(dt_adapter, live_monitor, wait_dt):
    # Arrange
    a1_id, a2_id = "light.schreibtisch_lampe", "light.amelie_lampe"
    feat1, feat2 = "state", "state"
    s_id, s_feat = "sensor.esp_c3_helligkeit", "state"

    # Act
    # --- Source Test Case ---
    await dt_adapter.set_feature_value(a1_id, feat1, "on")
    await dt_adapter.set_feature_value(a2_id, feat2, "off")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    source_out = float(await dt_adapter.get_feature_value(s_id, s_feat))

    # --- Follow-up Test Case ---
    await dt_adapter.set_feature_value(a1_id, feat1, "off")
    await dt_adapter.set_feature_value(a2_id, feat2, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    followup_out = float(await dt_adapter.get_feature_value(s_id, s_feat))

    # Assert
    return source_out, followup_out


@pytest.mark.asyncio
@pytest.mark.mr(
    type="stability",
    tolerance=0.05,  # allowed fluctuation range (5% of average value)
    duration=15.0    # measurement duration in seconds
)
async def test_sensor_stability(dt_adapter, live_monitor, wait_dt):
    # Act: Ensure light is OFF (so light sensor should be stable in dark room)
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

    # Wait for the system to settle before stability check begins
    await wait_dt()

    # Return the sensor and feature to be measured by the stability relation
    return "sensor.esp_c3_helligkeit", "state"


@pytest.mark.asyncio
@pytest.mark.mr(type="proportionality", tolerance=0.1)
async def test_light_proportionality(dt_adapter, wait_dt):
    """
    Checks if both illuminance sensors react proportionally when the desk lamp is turned on.
    Expects 4 return values: (S1, F1, S2, F2)
    """
    sensor1_id = "sensor.esp_c3_helligkeit"
    sensor2_id = "sensor.esp_c6_helligkeit"

    # 1. Source State: Baseline readings
    s1 = await dt_adapter.get_feature_value(sensor1_id, "state")
    s2 = await dt_adapter.get_feature_value(sensor2_id, "state")

    # 2. Action: Turn on the lamp
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "on")
    await wait_dt()

    # 3. Follow-up State: Readings after action
    f1 = await dt_adapter.get_feature_value(sensor1_id, "state")
    f2 = await dt_adapter.get_feature_value(sensor2_id, "state")

    return s1, f1, s2, f2


async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Ensuring baseline state after test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")
    await dt_adapter.set_feature_value("light.amelie_lampe", "state", "off")


    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "on")

