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

_MODULE_WAIT_DT = {}

@pytest_asyncio.fixture(scope="session")
def wait_time(request):
    return request.config.getoption("--wait-time")

@pytest_asyncio.fixture(scope="function")
async def wait_dt(request, wait_time):
    """Wait for the environment physics to catch up using the global wait time."""
    module_name = request.module.__name__
    actual_wait = _MODULE_WAIT_DT.get(module_name, wait_time)
    async def _wait():
        await asyncio.sleep(actual_wait)
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
    
    def get_current_wait():
        if hasattr(adapter, "_measured_latency") and adapter._measured_latency is not None:
            return adapter._measured_latency
        return wait_time

    async def _wait():
        await asyncio.sleep(get_current_wait())

    try:
        # Execute beforeAll
        err = None
        if hasattr(request.module, "beforeAll"):
            try:
                await _call_lifecycle_hook(request.module.beforeAll, adapter, _wait)
            except AssertionError as ae:
                err = str(ae)
            except Exception as e:
                err = f"Exception in beforeAll: {e}"
            
            if err is not None:
                pytest.fail(err, pytrace=False)
                
            # Store the measured latency for this module after beforeAll completes!
            if hasattr(adapter, "_measured_latency") and adapter._measured_latency is not None:
                _MODULE_WAIT_DT[request.module.__name__] = adapter._measured_latency
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
        err = None
        if hasattr(request.module, "beforeEach"):
            try:
                await _call_lifecycle_hook(request.module.beforeEach, dt_adapter, wait_dt)
            except AssertionError as ae:
                err = str(ae)
            except Exception as e:
                err = f"Exception in beforeEach: {e}"
            
            if err is not None:
                pytest.fail(err, pytrace=False)
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
