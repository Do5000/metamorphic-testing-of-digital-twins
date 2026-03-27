import asyncio
from mt_framework import DigitalTwinAdapter, ConservationRelation
from ut_helpers import UT_TENANT

async def run_light_conservation_test():
    # Wir nutzen den Adapter mit WebSocket für Befehle und HTTP für Status
    dt = DigitalTwinAdapter(http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2")
    
    print("====================================================")
    print("Metamorphic Test: Light Conservation -> Illuminance")
    print("====================================================\n")
    
    cons_rel = ConservationRelation()
    
    test_config = {
        'actuator_1_id': 'light.sueden_tuer',
        'actuator_2_id': 'light.norden_tuer',
        'feature': 'brightness',
        'sensor_id': 'Illuminance.Room518a_Ceiling',
        'sensor_feature': 'Illuminance',
        
        'initial_a': 100,           # Licht 1 auf 50% Helligkeit
        'initial_b': 0,           # Licht 2 auf 50% Helligkeit
        'delta': 100,               # Licht 1 wird dunkler (-30), Licht 2 wird heller (+30)
        
        'wait_time': 30.0,         # 30 Sekunden warten auf physikalische Reaktion
        'tolerance': 0.15          # 15% Abweichung sind erlaubt
    }
    
    print(f"Test: {cons_rel.name}")
    print(f"Description: {cons_rel.description}")
    print(f"Licht 1: {UT_TENANT}:{test_config['actuator_1_id']}")
    print(f"Licht 2: {UT_TENANT}:{test_config['actuator_2_id']}")
    print(f"Sensor:  {UT_TENANT}:{test_config['sensor_id']}")
    print("-" * 50)

    try:
        passed, msg = await cons_rel.execute(dt, test_config)
        
        print("\n" + "=" * 20)
        print(f"TEST RESULT: {'PASS' if passed else 'FAIL'}")
        print(f"REASON: {msg}")
        print("=" * 20)
        
    finally:
        await dt.close() # WebSocket sauber schließen

if __name__ == "__main__":
    asyncio.run(run_light_conservation_test())
