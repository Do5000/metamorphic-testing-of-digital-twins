import socket
import requests
import json
import asyncio
import websockets
from datetime import datetime

# configuration from ut_params.py
LOCAL_DITTO_WS = "ws://127.0.0.1:8082/ws/2"
LOCAL_DITTO_HTTP = "http://127.0.0.1:8083"
REAL_DITTO_HTTP = "http://127.0.0.1:8080"
HA_IP = "138.232.83.30"
HA_HTTP = f"http://{HA_IP}:8123"
MW_HTTP = f"http://{HA_IP}:8081"
MW_MQTT_PORT = 1884
HA_MQTT_PORT = 1885
HONO_MQTT_PORT = 1883 # usually 1883 or 8883

def check_port(ip, port, name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip, port))
    if result == 0:
        print(f"[OK]   {name} ({ip}:{port}) ist erreichbar.")
        return True
    else:
        print(f"[FAIL] {name} ({ip}:{port}) ist NICHT erreichbar. (Code: {result})")
        return False
    s.close()

def check_http(url, name, auth=None):
    try:
        resp = requests.get(url, auth=auth, timeout=5)
        print(f"[OK]   {name} ({url}) antwortet mit Status {resp.status_code}.")
        return True
    except Exception as e:
        print(f"[FAIL] {name} ({url}) Fehler: {e}")
        return False

async def check_ws(url, name):
    try:
        async with websockets.connect(url, open_timeout=5) as ws:
            print(f"[OK]   {name} ({url}) WebSocket Verbindung erfolgreich.")
            return True
    except Exception as e:
        print(f"[FAIL] {name} ({url}) WebSocket Fehler: {e}")
        return False

async def run_diagnostics():
    print("="*60)
    print(f"PIPELINE DIAGNOSE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\n--- STUFE 1: LOKALE DIENSTE (MOCK SERVER) ---")
    check_port("127.0.0.1", 8083, "Mock Ditto HTTP")
    check_port("127.0.0.1", 8082, "Mock Ditto WS")
    await check_ws(LOCAL_DITTO_WS, "Mock Ditto WS (Handshake)")
    
    print("\n--- STUFE 2: INFRASTRUKTUR (LIVING LAB) ---")
    check_port(HA_IP, 8081, "Middleware HTTP")
    check_port(HA_IP, 1884, "Middleware MQTT")
    check_port(HA_IP, 8123, "Home Assistant HTTP")
    check_port(HA_IP, 1885, "Home Assistant MQTT")
    
    print("\n--- STUFE 3: FUNKTIONSTESTS (HTTP STATUS) ---")
    check_http(MW_HTTP, "Middleware API")
    check_http(HA_HTTP, "Home Assistant API")
    
    # Test command trigger via middleware to see if it can reach HA
    print("\n--- STUFE 4: END-TO-END TEST (COMMAND RELAY) ---")
    url = f"{MW_HTTP}/middleware/command"
    payload = {
        "uuid": "cover.cover_norden",
        "parameters": [{"name": "current_position", "value": 60}]
    }
    try:
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code == 200:
            print("[OK]   Middleware konnte Befehl erfolgreich entgegennehmen.")
        elif resp.status_code == 500:
            print(f"[FAIL] Middleware meldet Fehler 500 (meistens HA nicht erreichbar): {resp.text}")
        else:
            print(f"[WARN] Middleware meldet Status {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[FAIL] Middleware Command Relay fehlgeschlagen: {e}")

    print("\n" + "="*60)
    print("DIAGNOSE BEENDET")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_diagnostics())
