import requests
import json
import os

# Configuration (matching DigitalTwinAdapter defaults)
HTTP_URL = "http://127.0.0.1:8083"
CATALOG_FILE = "device_catalog.json"

def discover_devices():
    print(f"[*] Discovering devices from {HTTP_URL}...")
    try:
        # Querying the search API of the mock backend (or real Ditto)
        response = requests.get(f"{HTTP_URL}/api/2/search/things", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            catalog = {}
            for item in items:
                # Remove the tenant prefix for easier use in tests if present
                full_id = item.get("thingId", "")
                short_id = full_id.split(":")[-1] if ":" in full_id else full_id
                
                catalog[short_id] = {
                    "full_id": full_id,
                    "features": list(item.get("features", {}).keys()),
                    "attributes": item.get("attributes", {})
                }
            
            with open(CATALOG_FILE, "w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=4)
            
            print(f"[+] Success! {len(catalog)} devices saved to {CATALOG_FILE}")
            for sid in catalog:
                print(f"    - {sid} (Features: {', '.join(catalog[sid]['features'])})")
        else:
            print(f"[!] Error: Backend returned status {response.status_code}")
            
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        print("    Make sure your Mock Backend is running!")

if __name__ == "__main__":
    discover_devices()
