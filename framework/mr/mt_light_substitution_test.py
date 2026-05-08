import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Vorbereitung der Umgebung")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "off")

@pytest.mark.asyncio
@pytest.mark.mr(type="substitution", profile="sensor_profile.json", tolerance=0.1)
async def test_sensor_substitution(dt_adapter, wait_dt):
    
    # ARRANGE      
    light_id = "light.schreibtisch_lampe"
    new_sensor_id = "sensor.arbeitsplatz_helligkeit" 
    neighbor_sensor_id = "sensor.arbeitsplatz_helligkeit_2"
    
    # 1. ACT
    target_brightness = 50
    await dt_adapter.set_feature_value(light_id, "brightness", target_brightness)
    
    await wait_dt()
    
    # 2. ACT 
    val_new = await dt_adapter.get_feature_value(new_sensor_id, "state")
    val_neighbor = await dt_adapter.get_feature_value(neighbor_sensor_id, "state")
    
    # ASSERT
    return val_new, val_neighbor

async def afterAll(dt_adapter):
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "on")
