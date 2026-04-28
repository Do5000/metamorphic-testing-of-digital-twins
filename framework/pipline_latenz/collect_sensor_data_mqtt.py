import asyncio
import time
import csv
import os
import sys
import json

# Add framework to path if necessary
sys.path.append(os.path.join(os.getcwd(), 'framework'))

from mt_framework import DigitalTwinAdapter
from ut_mqtt_endpoints import Middleware
from ut_params import *

# Configuration
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

class MQTTCollector:
    def __init__(self):
        self.dt = DigitalTwinAdapter(ws_url="ws://127.0.0.1:8082/ws/2")
        self.mw = Middleware()
        self.data_points = []
        self.trigger_time = 0.0
        self.current_values = {s: None for s in SENSOR_FEATURES}
        
        # Set up MQTT callback
        self.mw.on_device_param_updated = self.on_mqtt_message

    def on_mqtt_message(self, device, param, value):
        # The Middleware class from ut_mqtt_endpoints.py provides device and param
        if device in SENSOR_FEATURES:
            try:
                self.current_values[device] = float(value)
            except (ValueError, TypeError):
                pass

    async def run(self):
        print(f"Connecting to MQTT Middleware at {self.mw.ip}:{self.mw.mqtt_port}...")
        self.mw.connect_mqtt()
        
        print(f"Connecting to Ditto WebSocket at {self.dt.ws_url}...")
        await self.dt._get_ws()
        
        print(f"Ensuring {SWITCH_ID} is OFF before test...")
        await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
        await asyncio.sleep(2.0)
        
        print(f"Triggering {SWITCH_ID} -> ON...")
        self.trigger_time = time.perf_counter()
        await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 1)
        
        print(f"Recording snapshots from MQTT at {POLL_INTERVAL}s intervals for {RECORD_DURATION} seconds...")
        start_time = time.perf_counter()
        next_sample_time = start_time
        
        try:
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

                # MQTT is handled in a separate thread by paho-mqtt (loop_start())
                # so we just need to sleep a bit to keep this loop from spinning too fast
                await asyncio.sleep(min(0.01, next_sample_time - now if next_sample_time > now else 0.01))
                
        except KeyboardInterrupt:
            print("\nInterrupted.")
        finally:
            print(f"Ensuring {SWITCH_ID} is OFF after test...")
            await self.dt.set_feature_value(SWITCH_ID, SWITCH_FEATURE, 0)
            self.mw.disconnect_mqtt()
            await self.dt.close()
            self.save_csv()

    def save_csv(self):
        filename = "sensor_data_mqtt.csv"
        if not self.data_points:
            print("No data points collected via MQTT.")
            return

        keys = ["rel_time_ms", "sensor", "value"]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.data_points)
        
        print(f"Successfully saved {len(self.data_points)} data points to {filename}")

if __name__ == "__main__":
    collector = MQTTCollector()
    try:
        asyncio.run(collector.run())
    except KeyboardInterrupt:
        pass
