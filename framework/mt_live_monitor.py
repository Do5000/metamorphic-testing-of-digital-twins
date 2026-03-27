import asyncio
import sys
import time
from mt_framework import DigitalTwinAdapter
from ut_helpers import UT_TENANT

async def monitor_things(thing_ids):
    """
    Monitors a list of things and their features in real-time.
    """
    dt = DigitalTwinAdapter(http_url="http://127.0.0.1:8083")
    
    print("====================================================")
    print("Digital Twin: Live Sensor Monitor")
    print(f"Monitoring: {len(thing_ids)} things")
    print("Press Ctrl+C to stop")
    print("====================================================\n")

    try:
        while True:
            timestamp = time.strftime("%H:%M:%S")
            print(f"--- Snapshot at {timestamp} ---")
            
            for t_id in thing_ids:
                # Handle both short names and full thingIds
                clean_id = t_id
                if ":" in t_id:
                    clean_id = t_id.split(":")[-1]
                
                try:
                    state = await dt.get_state(clean_id)
                    
                    if 'features' in state:
                        for feat_name, feat_data in state['features'].items():
                            val = feat_data.get('properties', {}).get('value', 'N/A')
                            print(f"  > {clean_id} [{feat_name}]: {val}")
                    else:
                        print(f"  ? {clean_id}: No features found or device offline")
                
                except Exception as e:
                    print(f"  ! {clean_id}: Error fetching state ({e})")
            
            print("") # Newline for better readability
            await asyncio.sleep(1.0)
            
    except (asyncio.CancelledError, KeyboardInterrupt):
        # This is expected when stopping with Ctrl+C
        pass
    finally:
        await dt.close()
        print("\nMonitor stopped.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mt_live_monitor.py <thingId1> <thingId2> ...")
        print("Example: python mt_live_monitor.py light.norden_tuer Illuminance.Room518a_Ceiling")
        sys.exit(1)
        
    ids_to_monitor = sys.argv[1:]
    asyncio.run(monitor_things(ids_to_monitor))
