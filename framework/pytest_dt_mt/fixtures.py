import pytest
import pytest_asyncio
import inspect
import asyncio
from typing import Callable, Any, Optional

from .core import DigitalTwinAdapter, PreconditionFailedError
from .monitoring import LiveValueMonitor

_MODULE_WAIT_DT = {}
_CALIBRATION_REPORTS = {}

@pytest_asyncio.fixture(scope="function")
async def dt_adapter() -> DigitalTwinAdapter:
    """
    Provides a configured DigitalTwinAdapter instance.
    Automatically closes WebSocket connections after the test.
    """
    adapter = DigitalTwinAdapter()
    yield adapter
    await adapter.close()

@pytest.fixture(scope="function")
def live_monitor(request: pytest.FixtureRequest, dt_adapter: DigitalTwinAdapter) -> Callable:
    """
    Provides a factory to create LiveValueMonitor instances.
    Usage:
        async with live_monitor(device_id, feature_name):
            await asyncio.sleep(10)
    """
    verbose = request.config.getoption("--monitor")
    def _create_monitor(device_id: str, feature_name: str, interval: float = 1.0) -> LiveValueMonitor:
        return LiveValueMonitor(dt_adapter, device_id, feature_name, interval=interval, verbose=verbose)
    return _create_monitor

@pytest_asyncio.fixture(scope="session")
def waitTime(request: pytest.FixtureRequest) -> float:
    return request.config.getoption("--wait-time")

@pytest_asyncio.fixture(scope="function")
async def wait_dt(request: pytest.FixtureRequest, waitTime: float) -> Callable:
    """Wait for the environment physics to catch up using the global wait time."""
    module_name = request.module.__name__
    actual_wait = _MODULE_WAIT_DT.get(module_name, waitTime)
    async def _wait() -> None:
        await asyncio.sleep(actual_wait)
    return _wait

async def _call_lifecycle_hook(func: Callable, adapter: DigitalTwinAdapter, wait_dt_callable: Callable) -> None:
    sig = inspect.signature(func)
    kwargs = {}
    if "dt_adapter" in sig.parameters: kwargs["dt_adapter"] = adapter
    if "wait_dt" in sig.parameters: kwargs["wait_dt"] = wait_dt_callable
    
    if inspect.iscoroutinefunction(func):
        await func(**kwargs)
    else:
        func(**kwargs)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def dt_module_hooks(request: pytest.FixtureRequest) -> None:
    """Handles beforeAll and afterAll once per test file."""
    adapter = DigitalTwinAdapter()
    waitTime = request.config.getoption("--wait-time")
    
    def get_current_wait() -> float:
        if hasattr(adapter, "_measured_latency") and adapter._measured_latency is not None:
            return adapter._measured_latency
        return waitTime

    async def _wait() -> None:
        await asyncio.sleep(get_current_wait())

    # Execute beforeAll
    if hasattr(request.module, "beforeAll"):
        try:
            await _call_lifecycle_hook(request.module.beforeAll, adapter, _wait)
            
            if hasattr(adapter, "_measured_latency") and adapter._measured_latency is not None:
                _MODULE_WAIT_DT[request.module.__name__] = adapter._measured_latency
            if hasattr(adapter, "_calibration_results"):
                _CALIBRATION_REPORTS[request.module.__name__] = adapter._calibration_results
            
            await _wait()
        except PreconditionFailedError as pe:
            pytest.skip(str(pe))
            return
        except Exception as e:
            pytest.fail(f"Exception in beforeAll: {e}", pytrace=False)
            return

    yield

    # Execute afterAll
    if hasattr(request.module, "afterAll"):
        try:
            await _call_lifecycle_hook(request.module.afterAll, adapter, _wait)
            await _wait()
        except Exception as e:
            print(f"\n[ERROR] Error in afterAll hook: {e}")
            
    await adapter.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def dt_function_hooks(request: pytest.FixtureRequest, dt_adapter: DigitalTwinAdapter, wait_dt: Callable) -> None:
    """Handles beforeEach and afterEach around every test."""
    
    # Execute beforeEach
    if hasattr(request.module, "beforeEach"):
        try:
            await _call_lifecycle_hook(request.module.beforeEach, dt_adapter, wait_dt)
            await wait_dt()
        except PreconditionFailedError as pe:
            pytest.skip(str(pe))
            return
        except Exception as e:
            pytest.fail(f"Exception in beforeEach: {e}", pytrace=False)
            return
        
    yield 

    # Execute afterEach
    if hasattr(request.module, "afterEach"):
        try:
            await _call_lifecycle_hook(request.module.afterEach, dt_adapter, wait_dt)
            await wait_dt()
        except Exception as e:
            print(f"\n[ERROR] Error in afterEach hook: {e}")
            
    module_name = request.module.__name__
    if module_name != "test_dsl_runner":
        if hasattr(dt_adapter, "_measured_latency") and dt_adapter._measured_latency is not None:
            _MODULE_WAIT_DT[module_name] = max(_MODULE_WAIT_DT.get(module_name, 0.0), dt_adapter._measured_latency)
        if hasattr(dt_adapter, "_calibration_results") and dt_adapter._calibration_results:
            if module_name not in _CALIBRATION_REPORTS:
                _CALIBRATION_REPORTS[module_name] = []
            for res in dt_adapter._calibration_results:
                if res not in _CALIBRATION_REPORTS[module_name]:
                    _CALIBRATION_REPORTS[module_name].append(res)
