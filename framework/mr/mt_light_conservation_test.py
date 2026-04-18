import pytest
import asyncio

@pytest.mark.asyncio
@pytest.mark.mr(type="conservation")
async def test_light_sensor_conservation(dt_adapter, live_monitor, wait_dt):
    a1_id, a2_id = "light.sueden_tuer", "light.norden_tuer"
    feat = "brightness"
    s_id, s_feat = "Illuminance.Room518a_Ceiling", "Illuminance"
    delta = 100
    
    # Source
    await dt_adapter.set_feature_value(a1_id, feat, 100)
    await dt_adapter.set_feature_value(a2_id, feat, 0)
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    source_out = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    # Follow-up
    await dt_adapter.set_feature_value(a1_id, feat, 100 - delta)
    await dt_adapter.set_feature_value(a2_id, feat, 0 + delta)
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    followup_out = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    diff = abs(source_out - followup_out)
    max_allowed = max(max(source_out, followup_out), 1) * 0.15
    assert diff <= max_allowed, f"Conservation broken: {source_out} vs {followup_out}"
