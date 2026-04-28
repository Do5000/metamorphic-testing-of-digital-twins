import asyncio
import httpx
import websockets
import json
import os
import sys
import re

# Append parent dir so ut_helpers can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ut_helpers import UT_TENANT, DITTO_USER, DITTO_PW

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
