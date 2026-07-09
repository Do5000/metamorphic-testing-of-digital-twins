import asyncio
import json
import os
from typing import Any, Optional

from pytest_dt_mt.calibration import measure_latency
from .client import DittoClient

class PreconditionFailedError(Exception):
    pass

class DigitalTwinAdapter:
    """
    Adapter to interface with the Digital Twin backend for metamorphic testing.
    Delegates low-level communication to DittoClient.
    """
    def __init__(self, client: Optional[DittoClient] = None):
        self._client = client or DittoClient()
        
        # Load device catalog for validation
        self.catalog = {}
        if os.path.exists("device_catalog.json"):
            with open("device_catalog.json", "r") as f:
                self.catalog = json.load(f)

    def validate_device(self, device_id: str) -> None:
        """Strict validation: Fail the test if device_id is unknown."""
        device_id = device_id.strip()
        if not self.catalog:
            return
        
        if device_id not in self.catalog:
            error_msg = f"\n[ERROR] Device '{device_id}' NOT FOUND in catalog!\n"
            raise AssertionError(error_msg)

    async def close(self) -> None:
        await self._client.close()

    async def get_feature_value(self, device_id: str, feature_name: str, silent: bool = False) -> Any:
        """Return the value from cache if available, otherwise fetch from HTTP."""
        device_id = device_id.strip()
        self.validate_device(device_id)
        val = None
        if device_id in self._client.cache and feature_name in self._client.cache[device_id]:
            val = self._client.cache[device_id][feature_name]
        else:
            # Fallback to HTTP and populate cache
            device = await self._client.fetch_state(device_id)
            if 'features' in device and feature_name in device['features']:
                val = device['features'][feature_name]['properties']['value']
        
        if not silent:
            print(f"      [ACTION] Query {device_id} -> {feature_name}: {val}")
        return val

    async def set_feature_value(self, device_id: str, feature_name: str, value: Any) -> int:
        """Sends a command via WebSocket."""
        device_id = device_id.strip()
        self.validate_device(device_id)
        print(f"      [ACTION] {device_id} -> set {feature_name} = {value}")
        await self._client.send_command(device_id, feature_name, value)
        return 200

    async def require_precondition(self, device_id: str, feature_name: str, expected_value: Any, skipMessage: Optional[str] = None) -> None:
        """
        Checks if a precondition is met. If not, skips the test/module.
        Useful in beforeAll or beforeEach to ensure environmental conditions.
        """
        val = await self.get_feature_value(device_id, feature_name, silent=True)
        
        val_str = str(val).lower()
        exp_str = str(expected_value).lower()
        
        match = (val_str == exp_str)

        if not match:
            if skipMessage is None:
                skipMessage = f"Precondition failed: '{device_id}' ({feature_name}) is '{val}'"
            print(f"      [PRECONDITION FAILED] {skipMessage}")
            raise PreconditionFailedError(skipMessage)
        else:
            print(f"      [PRECONDITION MET] '{device_id}' ({feature_name}) is '{val}'")

    async def measure_latency(self, actuator: str, actuatorFeature: str, valOff: Any, valOn: Any, sensor: str, sensorFeature: str, toleranceFactor: float = 1.5, addSeconds: float = 1.0, timeout: float = 15.0, minChangePercent: Optional[float] = None, runs: int = 1) -> float:
        """
        Dynamically measures the system latency (time from actuator action to sensor response)
        using the Monotony Relation workflow.
        Supports multiple runs and aggregates the maximum calculated wait time across all runs and calls.
        """
        return await measure_latency(
            self,
            actuator,
            actuatorFeature,
            valOff,
            valOn,
            sensor,
            sensorFeature,
            toleranceFactor=toleranceFactor,
            addSeconds=addSeconds,
            timeout=timeout,
            minChangePercent=minChangePercent,
            runs=runs
        )
