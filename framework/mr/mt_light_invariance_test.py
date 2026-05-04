import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "off")


async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")


@pytest.mark.asyncio
@pytest.mark.mr(type="invariance", tolerance=0.05)
async def test_invariance(dt_adapter, live_monitor, wait_dt):
    # Arrange
    a_id, a_feat = "light.schreibtisch_lampe", "state"
    s_id, s_feat = "sensor.arbeitsplatz_helligkeit", "state"

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


async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")

    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "on")