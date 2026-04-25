import pytest
import asyncio

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "off")

    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("switch.fernseher_ecke_steckdose ", "state", "off")
    await dt_adapter.set_feature_value("light.vintage_lampe", "state", "off")
    

async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    
    

async def afterEach(dt_adapter):
    print("\n[HOOK] afterEach: Cleaning up after test")

async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Tearing down digital twin environment")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "on")

@pytest.mark.asyncio
@pytest.mark.mr(type="conservation")
async def test_light_sensor_conservation(dt_adapter, live_monitor, wait_dt):
    a1_id, a2_id = "light.vintage_lampe", "switch.fernseher_ecke_steckdose "
    feat1, feat2 = "state", "state"
    s_id, s_feat = "sensor.arbeitsplatz_helligkeit", "state"
    delta = 100
    

    # Source
    await dt_adapter.set_feature_value(a1_id, feat1, "on")
    await dt_adapter.set_feature_value(a2_id, feat2, "off")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    source_out = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    # Follow-up
    await dt_adapter.set_feature_value(a1_id, feat1, "off")
    await dt_adapter.set_feature_value(a2_id, feat2, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    followup_out = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    diff = abs(source_out - followup_out)
    max_allowed = max(max(source_out, followup_out), 1) * 0.15 #TODO: make this relative to the input values
    assert diff <= max_allowed, f"Conservation broken: {source_out} vs {followup_out}"
