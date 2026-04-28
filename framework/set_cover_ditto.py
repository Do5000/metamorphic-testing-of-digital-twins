import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter


async def set_cover(device_id: str, position_percent: int):
    adapter = DigitalTwinAdapter()

    # Umrechnung von Prozent (0-100) in Framework-Format (0.0 - 1.0)
    position_val = max(0, min(100, position_percent)) / 100.0

    try:
        # Wir nutzen das Feature 'position'
        await adapter.set_feature_value(device_id, "current_position", position_val)
        print(f"[+] Cover {device_id} set to {position_percent}%")

        await asyncio.sleep(0.5)
        await adapter.close()

    except Exception as e:
        print(f"[!] Fehler: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_cover_ditto.py <device_id> <position_0_100>")
        print("Beispiel: python set_cover_ditto.py cover.wohnzimmer_rollladen 50")
        sys.exit(1)

    target_device = sys.argv[1]
    try:
        pos = int(sys.argv[2])
    except ValueError:
        print("[!] Fehler: Position muss eine Zahl zwischen 0 und 100 sein.")
        sys.exit(1)

    asyncio.run(set_cover(target_device, pos))
