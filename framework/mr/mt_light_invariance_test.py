import asyncio
from mt_framework import DigitalTwinAdapter, InvarianceRelation
from ut_helpers import UT_TENANT

async def run_light_invariance_test():
    # Wir nutzen den Adapter mit WebSocket für Befehle und HTTP für Status
    dt = DigitalTwinAdapter(http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2")
    
    print("====================================================")
    print("Metamorphic Test: Light Invariance -> Illuminance")
    print("====================================================\n")
    
    inv_rel = InvarianceRelation()
    
    test_config = {
        'actuator_id': 'light.norden_tuer',
        'actuator_feature': 'brightness',
        'sensor_id': 'Illuminance.Room518a_Ceiling',
        'sensor_feature': 'Illuminance',
        
        'input_value': 80,         # Schalte Licht auf 80% Helligkeit
        'reset_value': 0,          # Setze zwischendurch auf 0 zurück
        
        'wait_time': 30.0,         # 30 Sekunden warten auf physikalische Reaktion
        'tolerance': 0.05          # 5% Abweichung sind erlaubt (z.B. durch Rauschen)
    }
    
    print(f"Test: {inv_rel.name}")
    print(f"Description: {inv_rel.description}")
    print(f"Actuator: {UT_TENANT}:{test_config['actuator_id']}")
    print(f"Sensor:   {UT_TENANT}:{test_config['sensor_id']}")
    print("-" * 50)

    try:
        passed, msg = await inv_rel.execute(dt, test_config)
        
        print("\n" + "=" * 20)
        print(f"TEST RESULT: {'PASS' if passed else 'FAIL'}")
        print(f"REASON: {msg}")
        print("=" * 20)
        
    finally:
        await dt.close() # WebSocket sauber schließen

if __name__ == "__main__":
    asyncio.run(run_light_invariance_test())
