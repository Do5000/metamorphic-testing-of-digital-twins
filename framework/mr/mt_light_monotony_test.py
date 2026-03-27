import asyncio
import httpx
from ut_helpers import UT_TENANT, DITTO_USER, DITTO_PW
from mt_framework import DigitalTwinAdapter, MonotonicityRelation

async def run_light_sensor_test():
    dt = DigitalTwinAdapter(http_url="http://127.0.0.1:8083")
    
    print("====================================================")
    print("Metamorphic Test: Light -> Sensor Intensity")
    print("====================================================\n")
    
    # Configuration for the test
    # Actuator: The switch that turns on all lights
    # Sensor: The light sensor we expect to react
    mono_rel = MonotonicityRelation()
    test_config = {
        'actuator_id': 'switch.licht_schalter',
        'actuator_feature': 'state',
        'sensor_id': 'TSL2_Keyboard_spec.Room518a_WP1',
        'sensor_feature': 'TSL2_Keyboard_spec',
        'initial_input': 0,        # Switch OFF
        'increased_input': 1,     # Switch ON
        'wait_time': 30.0           # Wait 30 seconds for the physical value to propagate through MQTT/Middleware
    }
    
    print(f"Test: {mono_rel.name}")
    print(f"Description: {mono_rel.description}")
    print(f"Actuator: {UT_TENANT}:{test_config['actuator_id']} ({test_config['actuator_feature']})")
    print(f"Sensor:   {UT_TENANT}:{test_config['sensor_id']} ({test_config['sensor_feature']})")
    print("-" * 50)

    try:
        passed, msg = await mono_rel.execute(dt, test_config)
        
        print("\n" + "=" * 20)
        print(f"TEST RESULT: {'PASS' if passed else 'FAIL'}")
        print(f"REASON: {msg}")
        print("=" * 20)
        
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        print("Tip: Make sure translationunit_mockbackend_middleware.py is running!")

if __name__ == "__main__":
    asyncio.run(run_light_sensor_test())
