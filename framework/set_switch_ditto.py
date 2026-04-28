import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter

async def set_switch(device_id: str, turn_on: bool):
    adapter = DigitalTwinAdapter()
    
    value = 1 if turn_on else 0
    state_str = "ON" if turn_on else "OFF"
    
    try:
        # Schalter haben in unserem System nur das Feature 'state'
        await adapter.set_feature_value(device_id, "state", value)
        print(f"[+] Switch {device_id} set to {state_str}")
        
        await asyncio.sleep(0.5)
        await adapter.close()
            
    except Exception as e:
        print(f"[!] Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_switch_ditto.py <device_id> <on|off>")
        print("Beispiel: python set_switch_ditto.py switch.vintage_steckdose on")
        sys.exit(1)
        
    target_device = sys.argv[1]
    action = sys.argv[2].lower()
    
    is_on = action not in ["aus", "off", "0"]
    asyncio.run(set_switch(target_device, is_on))
