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
@pytest.mark.mr(type="invariance")
async def test_light_sensor_invariance(dt_adapter, live_monitor, wait_dt):
    a_id, a_feat = "light.vintage_lampe", "state"
    s_id, s_feat = "sensor.arbeitsplatz_helligkeit", "state"
    
    # Evaluation 1
    await dt_adapter.set_feature_value(a_id, a_feat, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    out1 = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    # Interference / Reset
    await dt_adapter.set_feature_value(a_id, a_feat, "off")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    
    # Evaluation 2
    await dt_adapter.set_feature_value(a_id, a_feat, "on")
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    out2 = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    diff = abs(out1 - out2)
    max_allowed = max(max(out1, out2), 1) * 0.05
    assert diff <= max_allowed, f"Outputs differ beyond tolerance: {out1} vs {out2}"
