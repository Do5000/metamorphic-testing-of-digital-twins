import asyncio
import sys
from pytest_dt_mt.core import DigitalTwinAdapter


async def set_cover(device_id: str, position_percent: int = None, tilt_percent: int = None):
    adapter = DigitalTwinAdapter()

    try:
        if position_percent is not None:
            # Umrechnung von Prozent (0-100) in Framework-Format (0.0 - 1.0)
            pos_val = max(0, min(100, position_percent)) / 100.0
            await adapter.set_feature_value(device_id, "current_position", pos_val)
            print(f"[+] Cover {device_id} position set to {position_percent}%")

        if tilt_percent is not None:
            # Umrechnung von Prozent (0-100) in Framework-Format (0.0 - 1.0)
            tilt_val = max(0, min(100, tilt_percent)) / 100.0
            await adapter.set_feature_value(device_id, "current_tilt_position", tilt_val)
            print(f"[+] Cover {device_id} tilt set to {tilt_percent}%")

        await asyncio.sleep(0.5)
        await adapter.close()

    except Exception as e:
        print(f"[!] Fehler: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Verwendung: python set_cover_ditto.py <device_id> <position_0_100> [tilt_0_100]")
        print("Beispiel (nur Position): python set_cover_ditto.py cover.cover_norden 50")
        print("Beispiel (beides):       python set_cover_ditto.py cover.cover_norden 100 45")
        sys.exit(1)

    target_device = sys.argv[1]
    try:
        pos = int(sys.argv[2])
        tilt = int(sys.argv[3]) if len(sys.argv) > 3 else None
    except ValueError:
        print("[!] Fehler: Werte müssen Zahlen zwischen 0 und 100 sein.")
        sys.exit(1)

    asyncio.run(set_cover(target_device, pos, tilt))
