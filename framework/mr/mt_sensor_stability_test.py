import pytest

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Setting up digital twin environment for the module")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "off")


async def beforeEach(dt_adapter):
    print("\n[HOOK] beforeEach: Ensuring baseline state before test")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

@pytest.mark.asyncio
@pytest.mark.mr(
    type="stability",
    tolerance=0.05,              # allowed fluctuation range (5% of average value)
    duration=15.0,               # measurement duration in seconds
    sensor="sensor.esp_c3_helligkeit",
    sensor_feature="state"
)
async def test_sensor_stability(dt_adapter, live_monitor, wait_dt):
    # Act: Ensure light is OFF (so light sensor should be stable in dark room)
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    
    # Wait for the system to settle before stability check begins
    await wait_dt()
    
    # Return dummy value (or current value) since MR type="stability" handles measurement automatically
    return None

async def afterAll(dt_adapter, wait_dt):
    print("\n[HOOK] afterAll: Restoring state")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein ", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus ", "state", "on")
