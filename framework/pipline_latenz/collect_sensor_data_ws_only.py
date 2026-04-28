import asyncio
import time
import csv
import os
import sys
import json

# Add framework to path if necessary
sys.path.append(os.path.join(os.getcwd(), 'framework'))

from mt_framework import DigitalTwinAdapter
from ut_helpers import UT_TENANT

# Configuration
# Mapping sensor name to its primary feature based on user's JSON
SENSOR_FEATURES = [
    "Illuminance.Room518a_Ceiling",
    "TSL1_LowerScreen_spec.Room518a_WP1",
    "TSL1_LowerScreen_spec.Room518a_WP2",
    "TSL2_Keyboard_spec.Room518a_WP1",
    "TSL2_Keyboard_spec.Room518a_WP2",
    "TSL3_UpperScreen_spec.Room518a_WP1",
    "TSL3_UpperScreen_spec.Room518a_WP2",
    "TSL4_UpperScreen_spec.Room518a_WP1",
    "TSL4_UpperScreen_spec.Room518a_WP2",
]

SWITCH_ID = "switch.licht_schalter"
SWITCH_FEATURE = "state"
RECORD_DURATION = 30.0

POLL_INTERVAL = 0.1

class WSOnlyCollector:
    def __init__(self):
        self.dt = DigitalTwinAdapter(ws_url="ws://127.0.0.1:8082/ws/2")
        self.data_points = []
        self.trigger_time = 0.0
        self.current_values = {s: None for s in SENSOR_FEATURES}

    def handle_message(self, msg_text):
        try:
            data = json.loads(msg_text)
            topic = data.get("topic", "")
            
            if "/things/twin/events/modified" in topic:
                parts = topic.split('/')
                if len(parts) >= 2:
                    device = parts[1]
                    if device in SENSOR_FEATURES:
                        val_data = data.get("value")
                        
                        # Extract numeric value
                        value = None
                        if isinstance(val_data, dict):
                            if 'properties' in val_data and 'value' in val_data['properties']:
                                value = float(val_data['properties']['value'])
                        else:
                            try:
                                value = float(val_data)
                            except:
                                pass
                        
                        if value is not None:
                            self.current_values[device] = value
        except Exception:
            pass

    async def run(self):
        print(f"Connecting to {self.dt.ws_url}...")
        ws = await self.dt._get_ws()
        
        print(f"Ensuring {SWITCH_ID} is OFF before test...")
        await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
        await asyncio.sleep(2.0)
        
        print(f"Triggering {SWITCH_ID} -> ON...")
        self.trigger_time = time.perf_counter()
        await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 1)
        
        print(f"Recording snapshots at {POLL_INTERVAL}s intervals for {RECORD_DURATION} seconds...")
        start_time = time.perf_counter()
        next_sample_time = start_time
        
        while True:
            now = time.perf_counter()
            elapsed = now - start_time
            if elapsed >= RECORD_DURATION:
                break
            
            # Record a snapshot of all current values every POLL_INTERVAL
            if now >= next_sample_time:
                rel_time_ms = (next_sample_time - start_time) * 1000
                for s_id, val in self.current_values.items():
                    if val is not None:
                        self.data_points.append({
                            "rel_time_ms": round(rel_time_ms, 2),
                            "sensor": s_id,
                            "value": val
                        })
                next_sample_time += POLL_INTERVAL

            # Check for incoming events on the WebSocket with a short timeout
            try:
                # Use a small timeout to keep the sampling loop responsive
                remaining_to_next_sample = next_sample_time - time.perf_counter()
                timeout = max(0.001, min(remaining_to_next_sample, 0.01))
                message = await asyncio.wait_for(ws.recv(), timeout=timeout)
                self.handle_message(message)
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"Error during reception: {e}")
                break
        
        print(f"Ensuring {SWITCH_ID} is OFF after test...")
        await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
        await self.dt.close()
        self.save_csv()

    def save_csv(self):
        filename = "sensor_data_ws_only.csv"
        if not self.data_points:
            print("No data points collected via WebSocket events.")
            return

        keys = ["rel_time_ms", "sensor", "value"]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.data_points)
        
        print(f"Successfully saved {len(self.data_points)} data points to {filename}")

if __name__ == "__main__":
    collector = WSOnlyCollector()
    try:
        asyncio.run(collector.run())
    except KeyboardInterrupt:
        pass
