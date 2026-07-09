import asyncio
from typing import List, Tuple, Optional, Any

class LiveValueMonitor:
    """
    Background worker that polls a sensor value and logs it during the test.
    Helps identify timing issues or signal noise.
    """
    def __init__(self, adapter: Any, device_id: str, feature_name: str, interval: float = 1.0, verbose: bool = False):
        self.adapter = adapter
        self.device_id = device_id
        self.feature_name = feature_name
        self.interval = interval
        self.verbose = verbose
        self.history: List[Tuple[float, Any]] = []
        self._stop_event = asyncio.Event()
        self._task: Optional[asyncio.Task] = None

    async def _run(self) -> None:
        start_time = asyncio.get_event_loop().time()
        while not self._stop_event.is_set():
            val = await self.adapter.get_feature_value(self.device_id, self.feature_name, silent=True)
            elapsed = asyncio.get_event_loop().time() - start_time
            self.history.append((elapsed, val))
            # Optional: Live printing of progression
            if self.verbose:
                print(f"      [LIVE MONITOR] {self.device_id} @ {elapsed:4.1f}s: {val}", flush=True)
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
