import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pytest_dt_mt.core import DigitalTwinAdapter
from pytest_dt_mt.fixtures import _MODULE_WAIT_DT, wait_dt

@pytest.mark.asyncio
async def test_measure_latency_success():
    # Arrange
    adapter = DigitalTwinAdapter()
    
    # Mock WebSocket connect
    mock_ws = AsyncMock()
    adapter._get_ws = AsyncMock(return_value=mock_ws)
    
    # When turning ON the actuator, we directly update the cache for the sensor
    async def mock_set_feature(device_id, feature_name, value):
        if value == "on":
            adapter._cache["sensor.test"] = {"state": 25.0}
        return 200
        
    adapter.set_feature_value = mock_set_feature
    
    # Mock get_feature_value to return a baseline
    adapter.get_feature_value = AsyncMock(return_value=10.0)
    
    # Act
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        result = await adapter.measure_latency(
            actuator="light.test",
            actuator_feature="state",
            val_off="off",
            val_on="on",
            sensor="sensor.test",
            sensor_feature="state",
            tolerance_factor=1.5,
            add_seconds=1.0,
            timeout=2.0
        )
        
    # Assert
    assert result is not None
    assert adapter._measured_latency is not None
    assert adapter._measured_latency > 1.0  # (measured latency * 1.5) + 1.0
    print(f"\n[TEST SUCCESS] Measured Latency Result: {result:.3f}s")

@pytest.mark.asyncio
async def test_measure_latency_with_min_change_percent():
    # Arrange
    adapter = DigitalTwinAdapter()
    
    # Mock WebSocket connect
    mock_ws = AsyncMock()
    adapter._get_ws = AsyncMock(return_value=mock_ws)
    
    # Case A: Change is below 10% (from 100 to 105 is 5%)
    async def mock_set_feature_small(device_id, feature_name, value):
        if value == "on":
            adapter._cache["sensor.test"] = {"state": 105.0}
        return 200
        
    adapter.set_feature_value = mock_set_feature_small
    adapter.get_feature_value = AsyncMock(return_value=100.0)
    
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # We expect a timeout because 5% < 10% threshold
        result_fail = await adapter.measure_latency(
            actuator="light.test",
            actuator_feature="state",
            val_off="off",
            val_on="on",
            sensor="sensor.test",
            sensor_feature="state",
            min_change_percent=0.10, # 10%
            timeout=0.2
        )
    assert result_fail is None
    
    # Case B: Change is above 10% (from 100 to 115 is 15%)
    async def mock_set_feature_large(device_id, feature_name, value):
        if value == "on":
            adapter._cache["sensor.test"] = {"state": 115.0}
        return 200
        
    adapter.set_feature_value = mock_set_feature_large
    
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        # We expect a success because 15% >= 10% threshold
        result_success = await adapter.measure_latency(
            actuator="light.test",
            actuator_feature="state",
            val_off="off",
            val_on="on",
            sensor="sensor.test",
            sensor_feature="state",
            min_change_percent=0.10, # 10%
            timeout=2.0
        )
    assert result_success is not None
    assert adapter._measured_latency > 1.0
    print(f"\n[TEST SUCCESS] min_change_percent successfully filtered out <10% and accepted >=10%")

@pytest.mark.asyncio
async def test_measure_latency_multiple_runs_and_aggregation():
    # Arrange
    adapter = DigitalTwinAdapter()
    
    # Mock WebSocket connect
    mock_ws = AsyncMock()
    adapter._get_ws = AsyncMock(return_value=mock_ws)
    
    # Simulate a dynamic delay that decreases on subsequent runs to verify we pick the maximum latency
    run_count = 0
    async def mock_set_feature_runs(device_id, feature_name, value):
        nonlocal run_count
        if value == "on":
            run_count += 1
            # Run 1: sets the cache
            adapter._cache[device_id] = {"state": 25.0}
        return 200
        
    adapter.set_feature_value = mock_set_feature_runs
    adapter.get_feature_value = AsyncMock(return_value=10.0)
    
    # Act: 1. Measure with 3 runs (simulated as instant, but loop is executed 3 times)
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        res1 = await adapter.measure_latency(
            actuator="light.run_test",
            actuator_feature="state",
            val_off="off",
            val_on="on",
            sensor="light.run_test", # same for simplicity in mock
            sensor_feature="state",
            runs=3,
            tolerance_factor=1.5,
            add_seconds=1.0,
            timeout=2.0
        )
        
    assert run_count == 3  # verified 3 runs executed
    assert res1 is not None
    assert adapter._measured_latency == res1
    
    # Act: 2. Measure a second device/call that yields a HIGHER wait time
    # We will manually set a higher computed latency to simulate a slow device
    # Let's say device 2 computes a calculated wait of 5.5 seconds.
    async def mock_set_feature_slow(device_id, feature_name, value):
        if value == "on":
            adapter._cache["sensor.slow"] = {"state": 99.0}
        return 200
        
    adapter.set_feature_value = mock_set_feature_slow
    adapter.get_feature_value = AsyncMock(return_value=0.0)
    
    # We mock asyncio.get_event_loop().time to fake a slow response of 1.5 seconds!
    fake_time = 0.0
    def mock_time():
        nonlocal fake_time
        fake_time += 1.5 # Increments by 1.5 seconds on every call
        return fake_time
        
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
        with patch("asyncio.get_event_loop") as mock_get_loop:
            mock_loop_instance = MagicMock()
            mock_loop_instance.time = mock_time
            mock_get_loop.return_value = mock_loop_instance
            
            res2 = await adapter.measure_latency(
                actuator="light.slow",
                actuator_feature="state",
                val_off="off",
                val_on="on",
                sensor="sensor.slow",
                sensor_feature="state",
                tolerance_factor=1.5,
                add_seconds=1.0,
                timeout=10.0
            )
            
    # res2 calculated wait should be: (measured latency of 1.5s * 1.5) + 1.0 = 3.25s
    # res1 was 1.0s. So adapter._measured_latency should have taken res2 (3.25s) because 3.25 > 1.0!
    assert adapter._measured_latency == max(res1, res2)
    print(f"\n[TEST SUCCESS] Multiple runs executed successfully, and aggregated maximum wait time of {adapter._measured_latency:.3f}s across calls!")

@pytest.mark.asyncio
async def test_wait_dt_fixture_integration():
    # Set the dynamic latency for this specific module name
    module_name = "test_module_name"
    _MODULE_WAIT_DT[module_name] = 0.05
    
    # Create a mock request object to mimic pytest's request fixture
    mock_request = MagicMock()
    mock_request.module.__name__ = module_name
    
    # Resolve fixture using __wrapped__ to avoid direct-call detection
    wait_func = await wait_dt.__wrapped__(mock_request, wait_time=2.0)
    
    # Time the wait
    start = asyncio.get_event_loop().time()
    await wait_func()
    elapsed = asyncio.get_event_loop().time() - start
    
    # Assert it waited roughly 0.05 seconds
    assert 0.04 <= elapsed <= 0.15
    print(f"\n[TEST SUCCESS] wait_dt successfully waited {elapsed:.3f}s based on the module-specific latency of 0.05s")

@pytest.mark.asyncio
async def test_stability_relation_validation():
    from pytest_dt_mt.relations.stability import StabilityRelation
    
    # 1. Test Success Case: fluctuation stays within tolerance
    adapter = DigitalTwinAdapter()
    
    # Mock get_feature_value to return slightly fluctuating values
    vals = [10.0, 10.5, 9.8, 10.2, 10.0]
    idx = 0
    async def mock_get_val(device_id, feature_name, silent=True):
        nonlocal idx
        val = vals[idx % len(vals)]
        idx += 1
        return val
        
    adapter.get_feature_value = mock_get_val
    
    # This should pass (max 10.5 - min 9.8 = 0.7 <= tolerance 10% of ~10 = 1.0)
    relation_success = StabilityRelation(duration=1.5, tolerance=0.10, feature="state")
    await relation_success.evaluate(
        result=["sensor.test", "state"],
        dt_adapter=adapter
    )
    print("\n[TEST SUCCESS] Stability passed within tolerance.")
    
    # 2. Test Failure Case: fluctuation exceeds tolerance
    adapter_unstable = DigitalTwinAdapter()
    
    unstable_vals = [10.0, 12.5, 9.0, 10.2, 10.0]
    idx_unstable = 0
    async def mock_get_unstable_val(device_id, feature_name, silent=True):
        nonlocal idx_unstable
        val = unstable_vals[idx_unstable % len(unstable_vals)]
        idx_unstable += 1
        return val
        
    adapter_unstable.get_feature_value = mock_get_unstable_val
    
    # This should fail (max 12.5 - min 9.0 = 3.5 > tolerance 10% of ~10 = 1.0)
    from pytest_dt_mt.relations.base import MetamorphicRelationError
    relation_fail = StabilityRelation(duration=1.5, tolerance=0.10, feature="state")
    with pytest.raises(MetamorphicRelationError) as exc_info:
        await relation_fail.evaluate(
            result=["sensor.test", "state"],
            dt_adapter=adapter_unstable
        )
    assert "Fluctuation" in str(exc_info.value)
    print("[TEST SUCCESS] Stability failed correctly when exceeding tolerance.")

@pytest.mark.asyncio
async def test_inverted_relation_validation():
    from pytest_dt_mt.plugin import validate_mr_result
    
    # 1. Monotonicity normally passes if followup >= source (e.g. 10.0 -> 15.0)
    # If inverted (not=True), it should FAIL because the original relation passed.
    result_passing = [10.0, 15.0]
    
    with pytest.raises(pytest.fail.Exception) as exc_info:
        await validate_mr_result(result_passing, dt_adapter=None, type="monotonicity", **{"not": True})
    assert "expected to fail but passed" in str(exc_info.value)
    assert "Details: [MR CHECK] Monotonicity PASSED:" in str(exc_info.value)
    
    # 2. Monotonicity normally fails if followup < source (e.g. 15.0 -> 10.0)
    # If inverted (not=True), it should PASS (not raise any error) because the original relation failed.
    result_failing = [15.0, 10.0]
    await validate_mr_result(result_failing, dt_adapter=None, type="monotonicity", **{"not": True})
    
    print("\n[TEST SUCCESS] Inverted Monotonicity relation successfully validated!")

@pytest.mark.asyncio
async def test_dsl_runner_inverted_relation():
    from mt_engine.runner import DslRunner
    
    # Arrange: Mock DigitalTwinAdapter
    adapter = DigitalTwinAdapter()
    adapter.set_feature_value = AsyncMock(return_value=200)
    
    # We want a failing Monotonicity relation normally: e.g. followup goes down
    # so we return 100 for source and 50 for followup.
    sensor_vals = [100.0, 50.0]
    idx = 0
    async def mock_get_val(device_id, feature_name, silent=True):
        nonlocal idx
        val = sensor_vals[idx % len(sensor_vals)]
        idx += 1
        return val
    adapter.get_feature_value = mock_get_val
    adapter.validate_device = MagicMock()
    
    test_data = {
        "name": "test_monotony_not",
        "relation": "monotonicity",
        "not": True,
        "actuators": [{"deviceId": "light.test", "feature": "state"}],
        "sensors": [{"deviceId": "sensor.test", "feature": "state"}],
        "sourceActions": ["on"],
        "followupActions": ["off"],
    }
    
    runner = DslRunner(adapter, {})
    
    # Since 50 < 100, monotonicity fails. But since "not": True, execute_test should PASS.
    await runner.execute_test(test_data, AsyncMock())
    
    # Let's also check that if the relation unexpectedly passes (e.g. sensor values increase),
    # then with "not": True it should FAIL.
    sensor_vals_passing = [50.0, 100.0] # 100 >= 50
    idx_passing = 0
    async def mock_get_val_passing(device_id, feature_name, silent=True):
        nonlocal idx_passing
        val = sensor_vals_passing[idx_passing % len(sensor_vals_passing)]
        idx_passing += 1
        return val
    adapter.get_feature_value = mock_get_val_passing
    
    from pytest_dt_mt.relations.base import MetamorphicRelationError
    with pytest.raises(MetamorphicRelationError) as exc_info:
        await runner.execute_test(test_data, AsyncMock())
    assert "expected to fail but passed" in str(exc_info.value)
    assert "Details: [MR CHECK] Monotonicity PASSED:" in str(exc_info.value)
    
    print("\n[TEST SUCCESS] DslRunner inverted relation execution successfully validated!")


