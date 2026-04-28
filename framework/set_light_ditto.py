import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter

async def set_light(device_id: str, turn_on: bool):
    # Initialisiere den Adapter (nutzt standardmäßig 127.0.0.1:8083)
    adapter = DigitalTwinAdapter()
    
    value = 1 if turn_on else 0
    state_str = "ON" if turn_on else "OFF"
    
    try:
        # Wir nutzen den Adapter, um Status und Helligkeit zu setzen
        # Der Adapter kümmert sich automatisch um die WebSocket-Verbindung
        await adapter.set_feature_value(device_id, "state", value)
        await adapter.set_feature_value(device_id, "brightness", value)
        
        print(f"[+] Light {device_id} set to {state_str}")
        
        # Kurz warten, damit die Nachricht versendet wird
        await asyncio.sleep(0.5)
        await adapter.close()
            
    except Exception as e:
        print(f"[!] Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_light_ditto.py <device_id> <on|off>")
        print("Beispiel: python set_light_ditto.py light.schreibtisch_lampe on")
        sys.exit(1)
        
    target_device = sys.argv[1]
    action = sys.argv[2].lower()
    
    is_on = action not in ["aus", "off", "0"]
    asyncio.run(set_light(target_device, is_on))
