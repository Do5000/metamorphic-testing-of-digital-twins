import asyncio
import httpx
import websockets
import json
import os
import sys
import re

# Append parent dir so ut_helpers can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ut_params import UT_TENANT, DITTO_USER, DITTO_PW

class DigitalTwinAdapter:
    """
    Adapter to interface with the Digital Twin backend (Ditto).
    Uses a persistent WebSocket to listen for events and HTTP for initial state.
    """
    def __init__(self, http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2"):
        self.http_url = http_url
        self.ws_url = ws_url
        self._ws = None
        self._client = httpx.AsyncClient(verify=False, timeout=5.0)
        self._cache = {} # {device_id: {feature_name: value}}
        self._listen_task = None
        self._stop_listen = asyncio.Event()
        
        # Load device catalog for validation
        self.catalog = {}
        if os.path.exists("device_catalog.json"):
            with open("device_catalog.json", "r") as f:
                self.catalog = json.load(f)

    def validate_device(self, device_id):
        """Strict validation: Fail the test if device_id is unknown."""
        device_id = device_id.strip()
        if not self.catalog:
            return
        
        if device_id not in self.catalog:
            error_msg = f"\n[ERROR] Device '{device_id}' NOT FOUND in catalog!\n"
            raise AssertionError(error_msg)

    async def _get_ws(self):
        from websockets.protocol import State
        if self._ws is None or self._ws.state is not State.OPEN:
            self._ws = await websockets.connect(
                self.ws_url,
                ping_interval=20,
                ping_timeout=20
            )
            # If we just connected/reconnected, we might want to start listening
            if self._listen_task is None:
                self._listen_task = asyncio.create_task(self._listen_loop())
        return self._ws

    async def _listen_loop(self):
        """Background task that processes incoming WebSocket events."""
        while not self._stop_listen.is_set():
            try:
                ws = await self._get_ws()
                async for message in ws:
                    if self._stop_listen.is_set():
                        break
                    data = json.loads(message)
                    # Example topic: UT_TENANT/light.schreibtisch_lampe/things/twin/events/modified
                    if "events/modified" in data.get("topic", ""):
                        parts = data["topic"].split("/")
                        if len(parts) >= 2:
                            device_id = parts[1]
                            path = data.get("path", "")
                            value = data.get("value")
                            
                            # Match feature name from path /features/FEATURE/properties/value
                            match = re.search(r'/features/([^/]+)/', path)
                            if match:
                                feature_name = match.group(1)
                                if device_id not in self._cache:
                                    self._cache[device_id] = {}
                                self._cache[device_id][feature_name] = value
            except Exception:
                if not self._stop_listen.is_set():
                    await asyncio.sleep(1) # Backoff before reconnect
                else:
                    break

    async def close(self):
        self._stop_listen.set()
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        if self._ws:
            await self._ws.close()
            self._ws = None
        await self._client.aclose()

    async def get_state(self, device_id):
        """Fetch the full state of a thing, preferentially from cache."""
        # Note: Usually we want a fresh state if asking for the full thing, 
        # but for performance in monitors we look at cache.
        resp = await self._client.get(
            f'{self.http_url}/api/2/things/{UT_TENANT}:{device_id}',
            auth=(DITTO_USER, DITTO_PW)
        )
        data = resp.json()
        # Seed cache with this data
        if "features" in data:
            self._cache[device_id] = {
                k: v.get("properties", {}).get("value") 
                for k, v in data["features"].items()
            }
        return data
        
    async def get_feature_value(self, device_id, feature_name, silent=False):
        """Return the value from cache if available, otherwise fetch from HTTP."""
        device_id = device_id.strip()
        self.validate_device(device_id)
        val = None
        if device_id in self._cache and feature_name in self._cache[device_id]:
            val = self._cache[device_id][feature_name]
        else:
            # Fallback to HTTP and populate cache
            device = await self.get_state(device_id)
            if 'features' in device and feature_name in device['features']:
                val = device['features'][feature_name]['properties']['value']
        
        if not silent:
            print(f"      [ACTION] Query {device_id} -> {feature_name}: {val}")
        return val

    async def set_feature_value(self, device_id, feature_name, value):
        """Sends a command via WebSocket."""
        device_id = device_id.strip()
        self.validate_device(device_id)
        print(f"      [ACTION] {device_id} -> set {feature_name} = {value}")
        ws = await self._get_ws()
        msg = {
            "topic": f"{UT_TENANT}/{device_id}/things/live/messages/{feature_name}",
            "headers": {
                "content-type": "application/json",
                "response-required": False
            },
            "path": f"/inbox/messages/{feature_name}",
            "value": value
        }
        await ws.send(json.dumps(msg))
        return 200

    async def measure_latency(self, actuator, actuator_feature, val_off, val_on, sensor, sensor_feature, tolerance_factor=1.5, add_seconds=1.0, timeout=15.0, min_change_percent=None, runs=1):
        """
        Dynamically measures the system latency (time from actuator action to sensor response)
        using the Monotony Relation workflow.
        Supports multiple runs and aggregates the maximum calculated wait time across all runs and calls.
        """
        print(f"\n      [LATENCY CALIBRATION] Starting latency calibration...")
        print(f"      [LATENCY CALIBRATION] Actuator: {actuator} ({actuator_feature})")
        print(f"      [LATENCY CALIBRATION] Sensor: {sensor} ({sensor_feature})")
        if min_change_percent is not None:
            print(f"      [LATENCY CALIBRATION] Minimum change threshold: {min_change_percent * 100:.1f}%")
        if runs > 1:
            print(f"      [LATENCY CALIBRATION] Performing {runs} calibration runs...")
        
        # 1. Ensure WebSocket is connected and background listener task is active
        await self._get_ws()
        
        latencies = []
        
        for run_idx in range(1, runs + 1):
            run_label = f" (Run {run_idx}/{runs})" if runs > 1 else ""
            
            # 2. Set actuator to off state
            print(f"      [LATENCY CALIBRATION]{run_label} Setting actuator to baseline '{val_off}'...")
            await self.set_feature_value(actuator, actuator_feature, val_off)
            
            # 3. Wait to let the system stabilize and ensure baseline is reached
            await asyncio.sleep(3.0)
            
            # 4. Get the baseline sensor value and seed the cache
            baseline_val = await self.get_feature_value(sensor, sensor_feature, silent=True)
            print(f"      [LATENCY CALIBRATION]{run_label} Baseline sensor value: {baseline_val}")
            
            # 5. Trigger the change: setting actuator to on state
            print(f"      [LATENCY CALIBRATION]{run_label} Triggering change: setting actuator to '{val_on}'...")
            start_time = asyncio.get_event_loop().time()
            await self.set_feature_value(actuator, actuator_feature, val_on)
            
            # 6. Poll cache for change
            change_detected = False
            measured_latency = None
            poll_start = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - poll_start < timeout:
                # Retrieve from cache
                current_val = self._cache.get(sensor, {}).get(sensor_feature)
                if current_val is not None and current_val != baseline_val:
                    # Check for numeric difference to avoid minor jitter if float
                    try:
                        if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                            if min_change_percent is not None:
                                denominator = abs(baseline_val) if abs(baseline_val) > 0.001 else 1.0
                                relative_change = abs(current_val - baseline_val) / denominator
                                if relative_change < min_change_percent:
                                    await asyncio.sleep(0.02)
                                    continue
                            else:
                                if abs(current_val - baseline_val) < 0.001:
                                    await asyncio.sleep(0.02)
                                    continue
                    except Exception:
                        pass
                        
                    measured_latency = asyncio.get_event_loop().time() - start_time
                    change_detected = True
                    break
                await asyncio.sleep(0.02)
            
            if change_detected and measured_latency is not None:
                print(f"      [LATENCY CALIBRATION]{run_label} SUCCESS: Measured latency = {measured_latency:.3f}s")
                latencies.append(measured_latency)
            else:
                print(f"      [LATENCY CALIBRATION]{run_label} WARNING: Calibration timed out! No sensor change detected within {timeout}s.")
        
        if latencies:
            max_measured = max(latencies)
            calculated_wait = (max_measured * tolerance_factor) + add_seconds
            if runs > 1:
                print(f"      [LATENCY CALIBRATION] Calibration complete over {runs} runs.")
                print(f"      [LATENCY CALIBRATION] Max measured latency = {max_measured:.3f}s")
            print(f"      [LATENCY CALIBRATION] Calculated wait_dt (with {tolerance_factor}x factor + {add_seconds}s buffer) = {calculated_wait:.3f}s")
            
            # Keep the overall maximum wait time across multiple measure_latency calls!
            if getattr(self, "_measured_latency", None) is None:
                self._measured_latency = calculated_wait
            else:
                self._measured_latency = max(self._measured_latency, calculated_wait)
        else:
            print(f"      [LATENCY CALIBRATION] WARNING: All calibration runs timed out.")
            if getattr(self, "_measured_latency", None) is None:
                print(f"      [LATENCY CALIBRATION] Using default/fallback wait time.")
                self._measured_latency = None
            else:
                print(f"      [LATENCY CALIBRATION] Retaining previously measured maximum wait time of {self._measured_latency:.3f}s.")
        
        return self._measured_latency

class LiveValueMonitor:
    """
    Background worker that polls a sensor value and logs it during the test.
    Helps identify timing issues or signal noise.
    """
    def __init__(self, adapter, device_id, feature_name, interval=1.0, verbose=False):
        self.adapter = adapter
        self.device_id = device_id
        self.feature_name = feature_name
        self.interval = interval
        self.verbose = verbose
        self.history = []
        self._stop_event = asyncio.Event()
        self._task = None

    async def _run(self):
        start_time = asyncio.get_event_loop().time()
        while not self._stop_event.is_set():
            val = await self.adapter.get_feature_value(self.device_id, self.feature_name, silent=True)
            elapsed = asyncio.get_event_loop().time() - start_time
            self.history.append((elapsed, val))
            # Optional: Live printing of progression
            if self.verbose:
                print(f"      [LIVE MONITOR] {self.device_id} @ {elapsed:4.1f}s: {val}")
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                continue

    async def __aenter__(self):
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._task:
            await self._task
