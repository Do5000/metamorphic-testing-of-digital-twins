import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "off")

async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state (Light OFF)")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

@pytest.mark.asyncio
@pytest.mark.mr(type="proportionality", tolerance=0.2)
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
    print("\n[HOOK] afterAll: Restoring environment")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "on")
