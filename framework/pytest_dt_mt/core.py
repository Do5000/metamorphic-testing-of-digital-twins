import asyncio
import httpx
import websockets
import json
import os
import sys

# Append parent dir so ut_helpers can be imported easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ut_helpers import UT_TENANT, DITTO_USER, DITTO_PW

class DigitalTwinAdapter:
    """
    Adapter to interface with the Digital Twin backend (Ditto).
    Uses WebSockets for real-time commands and HTTP for state retrieval.
    """
    def __init__(self, http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2"):
        self.http_url = http_url
        self.ws_url = ws_url
        self._ws = None

    async def _get_ws(self):
        from websockets.protocol import State
        
        if self._ws is None or self._ws.state is not State.OPEN:
            # We add ping_interval and ping_timeout to keep the connection alive
            # during the wait periods.
            self._ws = await websockets.connect(
                self.ws_url,
                ping_interval=20,  # Send a ping every 20 seconds
                ping_timeout=20    # Wait 20 seconds for a pong response
            )
        return self._ws

    async def close(self):
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def get_state(self, device_id):
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(
                f'{self.http_url}/api/2/things/{UT_TENANT}:{device_id}',
                auth=(DITTO_USER, DITTO_PW)
            )
            return resp.json()
        
    async def get_feature_value(self, device_id, feature_name):
        device = await self.get_state(device_id)
        if 'features' in device and feature_name in device['features']:
            return device['features'][feature_name]['properties']['value']
        return None

    async def set_feature_value(self, device_id, feature_name, value):
        """
        Sends a command via WebSocket
        """
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
        return 200 # Success status code

class LiveValueMonitor:
    """
    Background worker that polls a sensor value and logs it during the test.
    Helps identify timing issues or signal noise.
    """
    def __init__(self, adapter, device_id, feature_name, interval=1.0):
        self.adapter = adapter
        self.device_id = device_id
        self.feature_name = feature_name
        self.interval = interval
        self.history = []
        self._stop_event = asyncio.Event()
        self._task = None

    async def _run(self):
        start_time = asyncio.get_event_loop().time()
        while not self._stop_event.is_set():
            val = await self.adapter.get_feature_value(self.device_id, self.feature_name)
            elapsed = asyncio.get_event_loop().time() - start_time
            self.history.append((elapsed, val))
            # Optional: Live printing of progression
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
