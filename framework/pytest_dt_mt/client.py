import asyncio
import httpx
import websockets
import json
import re
from typing import Optional, Dict, Any, AsyncGenerator

from .config import UT_TENANT, DITTO_USER, DITTO_PW, DITTO_NGINX_IP

class DittoClient:
    """
    Low-level client for Ditto API and WebSockets.
    """
    def __init__(self, http_url: str = f"http://{DITTO_NGINX_IP}:8083", ws_url: str = f"ws://{DITTO_NGINX_IP}:8082/ws/2"):
        self.http_url = http_url
        self.ws_url = ws_url
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._client = httpx.AsyncClient(verify=False, timeout=5.0)
        self._listen_task: Optional[asyncio.Task] = None
        self._stop_listen = asyncio.Event()
        # Shared cache injected from adapter or kept locally if client manages it
        self.cache: Dict[str, Dict[str, Any]] = {} 

    async def get_ws(self) -> websockets.WebSocketClientProtocol:
        from websockets.protocol import State
        if self._ws is None or self._ws.state is not State.OPEN:
            self._ws = await websockets.connect(
                self.ws_url,
                ping_interval=20,
                ping_timeout=20
            )
            if self._listen_task is None:
                self._listen_task = asyncio.create_task(self._listen_loop())
        return self._ws

    async def _listen_loop(self) -> None:
        """Background task that processes incoming WebSocket events."""
        while not self._stop_listen.is_set():
            try:
                ws = await self.get_ws()
                async for message in ws:
                    if self._stop_listen.is_set():
                        break
                    data = json.loads(message)
                    if "events/modified" in data.get("topic", ""):
                        parts = data["topic"].split("/")
                        if len(parts) >= 2:
                            device_id = parts[1]
                            path = data.get("path", "")
                            value = data.get("value")
                            
                            match = re.search(r'/features/([^/]+)/', path)
                            if match:
                                feature_name = match.group(1)
                                if device_id not in self.cache:
                                    self.cache[device_id] = {}
                                self.cache[device_id][feature_name] = value
            except Exception:
                if not self._stop_listen.is_set():
                    await asyncio.sleep(1)
                else:
                    break

    async def close(self) -> None:
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

    async def fetch_state(self, device_id: str) -> Dict[str, Any]:
        """Fetch the full state of a thing via HTTP."""
        resp = await self._client.get(
            f'{self.http_url}/api/2/things/{UT_TENANT}:{device_id}',
            auth=(DITTO_USER, DITTO_PW)
        )
        data = resp.json()
        if "features" in data:
            self.cache[device_id] = {
                k: v.get("properties", {}).get("value") 
                for k, v in data["features"].items()
            }
        return data

    async def send_command(self, device_id: str, feature_name: str, value: Any) -> None:
        """Sends a command via WebSocket."""
        ws = await self.get_ws()
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
