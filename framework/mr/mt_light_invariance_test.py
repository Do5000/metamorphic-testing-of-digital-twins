import pytest
import asyncio

@pytest.mark.asyncio
@pytest.mark.mr(type="invariance")
async def test_light_sensor_invariance(dt_adapter, live_monitor, wait_dt):
    a_id, a_feat = "light.norden_tuer", "brightness"
    s_id, s_feat = "Illuminance.Room518a_Ceiling", "Illuminance"
    
    # Evaluation 1
    await dt_adapter.set_feature_value(a_id, a_feat, 80)
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    out1 = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    # Interference / Reset
    await dt_adapter.set_feature_value(a_id, a_feat, 0)
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    
    # Evaluation 2
    await dt_adapter.set_feature_value(a_id, a_feat, 80)
    async with live_monitor(s_id, s_feat):
        await wait_dt()
    out2 = float(await dt_adapter.get_feature_value(s_id, s_feat))
    
    diff = abs(out1 - out2)
    max_allowed = max(max(out1, out2), 1) * 0.05
    assert diff <= max_allowed, f"Outputs differ beyond tolerance: {out1} vs {out2}"
