import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter

async def set_pir(device_id: str, input_val: str):
    adapter = DigitalTwinAdapter()
    
    try:
        # Konvertiere Input (z.B. 1/0, on/off, true/false) in 1.0 oder 0.0
        is_active = input_val.lower() in ["1", "on", "true", "active"]
        state_val = 1.0 if is_active else 0.0
        
        await adapter.set_feature_value(device_id, "PIR", state_val)
        print(f"[+] PIR {device_id} -> State: {'ACTIVE' if is_active else 'INACTIVE'} ({state_val})")
        
        await asyncio.sleep(0.5)
        await adapter.close()
            
    except Exception as e:
        print(f"[!] Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_pir_ditto.py <device_id> <on|off|1|0>")
        print("Beispiele:")
        print("  python set_pir_ditto.py PIR.Room518a_Ceiling 1")
        sys.exit(1)
        
    target_device = sys.argv[1]
    val = sys.argv[2]
    
    asyncio.run(set_pir(target_device, val))
