import asyncio
import json
import websockets
import sys

# Konfiguration
WS_URL = "ws://127.0.0.1:8082/ws/2" 
UT_TENANT = "at.uibk.ut.tenants"

async def send_command(device_id: str, turn_on: bool):
    # 1 bedeutet AN, 0 bedeutet AUS
    value = 1 if turn_on else 0
    state_str = "ON" if turn_on else "OFF"
    
    print(f"Verbinde mit {WS_URL} ...")
    try:
        async with websockets.connect(WS_URL) as ws:
            # Ein Schalter (Switch) hat nur das Feature "state"
            msg_state = {
                "topic": f"{UT_TENANT}/{device_id}/things/live/messages/state",
                "headers": {
                    "content-type": "application/json",
                    "response-required": False
                },
                "path": "/inbox/messages/state",
                "value": value
            }
            
            print(f"Sende Befehl: Schalte Status von [{device_id}] auf {state_str} (Zahlenwert: {value})")
            
            # Abschicken!
            await ws.send(json.dumps(msg_state))
            print("Befehl erfolgreich gesendet!")
            
            await asyncio.sleep(0.5)
            
    except ConnectionRefusedError:
        print(f"FEHLER: Der Mock-Server läuft nicht! Bitte starte erst translationunit_mockbackend_middleware.py in einem anderen Terminal.")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_switch_ditto.py <device_id> <on|off>")
        print("Beispiel: python set_switch_ditto.py switch.licht_schalter on")
        sys.exit(1)
        
    device_id = sys.argv[1]
    action = sys.argv[2].lower()
    
    if action in ["aus", "off", "0"]:
        asyncio.run(send_command(device_id, False))
    else:
        asyncio.run(send_command(device_id, True))
