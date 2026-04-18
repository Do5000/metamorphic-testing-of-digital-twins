import pytest
import pytest_asyncio
from .core import DigitalTwinAdapter, LiveValueMonitor

@pytest_asyncio.fixture(scope="function")
async def dt_adapter():
    """
    Provides a configured DigitalTwinAdapter instance.
    Automatically closes WebSocket connections after the test.
    """
    adapter = DigitalTwinAdapter()
    yield adapter
    await adapter.close()

@pytest.fixture(scope="function")
def live_monitor(dt_adapter):
    """
    Provides a factory to create LiveValueMonitor instances.
    Usage:
        async with live_monitor(device_id, feature_name):
            await asyncio.sleep(10)
    """
    def _create_monitor(device_id, feature_name, interval=1.0):
        return LiveValueMonitor(dt_adapter, device_id, feature_name, interval=interval)
    return _create_monitor

import asyncio

@pytest_asyncio.fixture(scope="session")
def wait_time(request):
    return request.config.getoption("--wait-time")

@pytest_asyncio.fixture(scope="function")
async def wait_dt(wait_time):
    """Wait for the environment physics to catch up using the global wait time."""
    async def _wait():
        await asyncio.sleep(wait_time)
    return _wait
