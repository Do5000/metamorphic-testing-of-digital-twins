import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter

async def set_light(device_id: str, input_val: str):
    adapter = DigitalTwinAdapter()
    
    try:
        # Prüfen, ob die Eingabe eine Zahl (Helligkeit) ist
        if input_val.isdigit():
            percent = int(input_val)
            brightness_val = max(0, min(100, percent)) / 100.0
            state_val = 1 if percent > 0 else 0
            
            await adapter.set_feature_value(device_id, "state", state_val)
            await adapter.set_feature_value(device_id, "brightness", brightness_val)
            print(f"[+] Light {device_id} -> Brightness: {percent}% | State: {state_val}")
        
        else:
            # Eingabe ist ein Text-Befehl (on/off)
            is_on = input_val.lower() not in ["aus", "off", "0"]
            state_val = 1 if is_on else 0
            brightness_val = 1.0 if is_on else 0.0
            
            await adapter.set_feature_value(device_id, "state", state_val)
            await adapter.set_feature_value(device_id, "brightness", brightness_val)
            print(f"[+] Light {device_id} -> State: {'ON' if is_on else 'OFF'} (Brightness synced)")

        await asyncio.sleep(0.5)
        await adapter.close()
            
    except Exception as e:
        print(f"[!] Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_light_ditto.py <device_id> <on|off|0-100>")
        print("Beispiele:")
        print("  python set_light_ditto.py light.schreibtisch_lampe on")
        print("  python set_light_ditto.py light.schreibtisch_lampe 50")
        sys.exit(1)
        
    target_device = sys.argv[1]
    val = sys.argv[2]
    
    asyncio.run(set_light(target_device, val))
