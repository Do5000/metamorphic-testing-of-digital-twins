import pytest
import pytest_asyncio
import inspect
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
def live_monitor(request, dt_adapter):
    """
    Provides a factory to create LiveValueMonitor instances.
    Usage:
        async with live_monitor(device_id, feature_name):
            await asyncio.sleep(10)
    """
    verbose = request.config.getoption("--monitor")
    def _create_monitor(device_id, feature_name, interval=1.0):
        return LiveValueMonitor(dt_adapter, device_id, feature_name, interval=interval, verbose=verbose)
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

async def _call_lifecycle_hook(func, adapter, wait_dt):
    sig = inspect.signature(func)
    kwargs = {}
    if "dt_adapter" in sig.parameters: kwargs["dt_adapter"] = adapter
    if "wait_dt" in sig.parameters: kwargs["wait_dt"] = wait_dt
    
    if inspect.iscoroutinefunction(func):
        await func(**kwargs)
    else:
        func(**kwargs)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def dt_module_hooks(request):
    """Handles beforeAll and afterAll once per test file."""
    # Setup dependencies for module-scope
    adapter = DigitalTwinAdapter()
    wait_time = request.config.getoption("--wait-time")
    async def _wait():
        await asyncio.sleep(wait_time)

    try:
        # Execute beforeAll
        if hasattr(request.module, "beforeAll"):
            await _call_lifecycle_hook(request.module.beforeAll, adapter, _wait)
            await _wait() # Automatically wait after beforeAll

        yield # Let all tests in the module run

    finally:
        # Execute afterAll
        if hasattr(request.module, "afterAll"):
            try:
                await _call_lifecycle_hook(request.module.afterAll, adapter, _wait)
                await _wait()
            except Exception as e:
                print(f"\n[ERROR] Error in afterAll hook: {e}")
            
        await adapter.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def dt_function_hooks(request, dt_adapter, wait_dt):
    """Handles beforeEach and afterEach around every test."""
    
    try:
        # Execute beforeEach
        if hasattr(request.module, "beforeEach"):
            await _call_lifecycle_hook(request.module.beforeEach, dt_adapter, wait_dt)
            await wait_dt() # Automatically wait after beforeEach
        
        yield # Let the individual test run

    finally:
        # Execute afterEach
        if hasattr(request.module, "afterEach"):
            try:
                await _call_lifecycle_hook(request.module.afterEach, dt_adapter, wait_dt)
                await wait_dt()
            except Exception as e:
                print(f"\n[ERROR] Error in afterEach hook: {e}")
