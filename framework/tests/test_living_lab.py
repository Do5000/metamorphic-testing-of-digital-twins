import pytest


async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")

async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("switch.licht_schalter", "state", "off")
    await dt_adapter.set_feature_value("cover.cover_sueden", "current_position", 0)
    await dt_adapter.set_feature_value("cover.cover_norden", "current_position", 0)


@pytest.mark.asyncio
@pytest.mark.mr(type="monotonicity")
async def test_uni_monotony(dt_adapter, live_monitor, wait_dt):
    # Arrange
    actuator = "switch.licht_schalter"
    actuator_feature = "state"

    sensor = "Illuminance.Room518a_Ceiling"
    sensor_feature = "Illuminance"

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
async def test_uni_invariance(dt_adapter, live_monitor, wait_dt):
    # Arrange
    a_id, a_feat = "switch.licht_schalter", "state"
    s_id, s_feat = "Illuminance.Room518a_Ceiling", "Illuminance"

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
async def test_uni_conservation(dt_adapter, live_monitor, wait_dt):
    # Arrange
    a1_id, a2_id = "light.sueden_tuer", "light.norden_tuer"
    feat1, feat2 = "state", "state"
    s_id, s_feat = "Illuminance.Room518a_Ceiling", "Illuminance"

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


async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("switch.licht_schalter", "state", "off")
    await dt_adapter.set_feature_value("cover.cover_sueden", "current_position", 0)
    await dt_adapter.set_feature_value("cover.cover_norden", "current_position", 0)