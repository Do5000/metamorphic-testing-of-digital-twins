import asyncio
import time
import csv
import os
import sys
from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

# Add framework to path if necessary
sys.path.append(os.path.join(os.getcwd(), 'framework'))

from pytest_dt_mt.core import DigitalTwinAdapter
from ut_helpers import UT_TENANT

# Configuration
# Mapping sensor name to its primary feature based on user's JSON
SENSOR_FEATURES = {
    "sensor.arbeitsplatz_helligkeit": "state",
}

SWITCH_ID = "light.schreibtisch_lampe"
SWITCH_FEATURE = "state"
RECORD_DURATION = 30.0
POLL_INTERVAL = 0.1  # Poll every 100ms

async def run_collection():
    dt = DigitalTwinAdapter(http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2")
    
    data_points = []
    
    print(f"Ensuring {SWITCH_ID} is OFF before test...")
    await dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
    await asyncio.sleep(2.0) # Wait for it to settle

    print(f"Triggering {SWITCH_ID} -> ON...")
    # Send trigger command
    await dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 1)
    
    start_time = time.perf_counter()
    
    print(f"Recording for {RECORD_DURATION} seconds with {POLL_INTERVAL}s interval...")
    
    try:
        end_time = start_time + RECORD_DURATION
        while time.perf_counter() < end_time:
            loop_start = time.perf_counter()
            elapsed_ms = (loop_start - start_time) * 1000
            
            # Poll all sensors in parallel
            tasks = []
            sensor_names = list(SENSOR_FEATURES.keys())
            for s_name in sensor_names:
                tasks.append(dt.get_feature_value(s_name, SENSOR_FEATURES[s_name]))
            
            values = await asyncio.gather(*tasks, return_exceptions=True)
            
            for s_name, val in zip(sensor_names, values):
                if not isinstance(val, Exception) and val is not None:
                    data_points.append({
                        "rel_time_ms": round(elapsed_ms, 2),
                        "sensor": s_name,
                        "value": val
                    })
            
            # Control polling rate
            sleep_time = POLL_INTERVAL - (time.perf_counter() - loop_start)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
                
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        print(f"Ensuring {SWITCH_ID} is OFF after test...")
        await dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
        await dt.close()
        save_csv(data_points)

def save_csv(data_points):
    filename = "sensor_data_ws_http_raspi.csv"
    if not data_points:
        print("No data collected.")
        return

    keys = ["rel_time_ms", "sensor", "value"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data_points)
    
    print(f"Successfully saved {len(data_points)} data points to {filename}")

if __name__ == "__main__":
    try:
        asyncio.run(run_collection())
    except KeyboardInterrupt:
        pass
