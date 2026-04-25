import requests
import json
import os
import sys

# Konfiguration (aus deinem Backend übernommen)
RASPI_IP = "192.168.8.30"
RASPI_HTTP_PORT = 8123
RASPI_HA_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NzA4YmQ4MjViMzg0YWM1ODQ1NWExNWMyYWM1MmE3OSIsImlhdCI6MTc3NzE0MTI3NSwiZXhwIjoyMDkyNTAxMjc1fQ.lHLlrdOIT1CGg-1pv8c-I6Z88Xdv9_jwHEwjKdsPLdI"

def list_entities():
    print(f"[*] Frage Entitäten von HA ({RASPI_IP}) ab...")
    try:
        response = requests.get(
            f'http://{RASPI_IP}:{RASPI_HTTP_PORT}/api/states',
            headers={
                'Authorization': RASPI_HA_TOKEN,
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            states = response.json()
            print(f"\n{'Entity ID':<50} | {'Zustand':<15}")
            print("-" * 70)
            
            # Sortieren nach Domain für bessere Übersicht
            states.sort(key=lambda x: x['entity_id'])
            
            for s in states:
                e_id = s['entity_id']
                state = s['state']
                print(f"{e_id:<50} | {state:<15}")
                
            print(f"\n[+] Insgesamt {len(states)} Entitäten gefunden.")
        else:
            print(f"[!] Fehler: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"[!] Verbindungsfehler: {e}")

if __name__ == "__main__":
    list_entities()
