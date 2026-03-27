import asyncio
import json
import websockets
import sys

# Konfiguration
WS_URL = "ws://127.0.0.1:8082/ws/2" 
UT_TENANT = "at.uibk.ut.tenants"

async def send_command(device_id: str, position: int):
    print(f"Verbinde mit {WS_URL} ...")
    try:
        async with websockets.connect(WS_URL) as ws:
            # Ein Rollladen (Cover/Blind) hat das Feature "current_position"
            msg_position = {
                "topic": f"{UT_TENANT}/{device_id}/things/live/messages/current_position",
                "headers": {
                    "content-type": "application/json",
                    "response-required": False
                },
                "path": "/inbox/messages/current_position",
                "value": position
            }
            
            print(f"Sende Befehl: Schließe/Öffne Rollladen [{device_id}] auf Position: {position}%")
            
            # Abschicken
            await ws.send(json.dumps(msg_position))
            print("Befehl erfolgreich gesendet!")
            
            await asyncio.sleep(0.5)
            
    except ConnectionRefusedError:
        print(f"FEHLER: Der Mock-Server läuft nicht! Bitte starte erst translationunit_mockbackend_middleware.py in einem anderen Terminal.")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_cover_ditto.py <device_id> <position>")
        print("Beispiel: python set_cover_ditto.py cover.cover_norden 50")
        sys.exit(1)
        
    device_id = sys.argv[1]
    try:
        position = int(sys.argv[2])
    except ValueError:
        print("FEHLER: Die Position muss eine ganze Zahl (0-100) sein.")
        sys.exit(1)
        
    asyncio.run(send_command(device_id, position))
