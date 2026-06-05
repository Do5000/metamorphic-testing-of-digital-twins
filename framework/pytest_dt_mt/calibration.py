import asyncio

async def measure_latency(
    adapter,
    actuator,
    actuator_feature,
    val_off,
    val_on,
    sensor,
    sensor_feature,
    tolerance_factor=1.5,
    add_seconds=1.0,
    timeout=15.0,
    min_change_percent=None,
    runs=1
):
    """
    Dynamically measures the system latency (time from actuator action to sensor response)
    using the Monotony Relation workflow.
    Supports multiple runs and aggregates the maximum calculated wait time across all runs and calls.
    """
    print(f"\n      [LATENCY CALIBRATION] Starting latency calibration...")
    print(f"      [LATENCY CALIBRATION] Actuator: {actuator} ({actuator_feature})")
    print(f"      [LATENCY CALIBRATION] Sensor: {sensor} ({sensor_feature})")
    if min_change_percent is not None:
        print(f"      [LATENCY CALIBRATION] Minimum change threshold: {min_change_percent * 100:.1f}%")
    if runs > 1:
        print(f"      [LATENCY CALIBRATION] Performing {runs} calibration runs...")
    
    # 1. Ensure WebSocket is connected and background listener task is active
    await adapter._get_ws()
    
    latencies = []
    
    for run_idx in range(1, runs + 1):
        run_label = f" (Run {run_idx}/{runs})" if runs > 1 else ""
        
        # 2. Set actuator to off state
        print(f"      [LATENCY CALIBRATION]{run_label} Setting actuator to baseline '{val_off}'...")
        await adapter.set_feature_value(actuator, actuator_feature, val_off)
        
        # 3. Wait to let the system stabilize and ensure baseline is reached
        await asyncio.sleep(3.0)
        
        # 4. Get the baseline sensor value and seed the cache
        baseline_val = await adapter.get_feature_value(sensor, sensor_feature, silent=True)
        print(f"      [LATENCY CALIBRATION]{run_label} Baseline sensor value: {baseline_val}")
        
        # 5. Trigger the change: setting actuator to on state
        print(f"      [LATENCY CALIBRATION]{run_label} Triggering change: setting actuator to '{val_on}'...")
        start_time = asyncio.get_event_loop().time()
        await adapter.set_feature_value(actuator, actuator_feature, val_on)
        
        # 6. Poll cache for change
        change_detected = False
        measured_latency = None
        poll_start = asyncio.get_event_loop().time()
        
        while asyncio.get_event_loop().time() - poll_start < timeout:
            # Retrieve from cache
            current_val = adapter._cache.get(sensor, {}).get(sensor_feature)
            if current_val is not None and current_val != baseline_val:
                # Check for numeric difference to avoid minor jitter if float
                try:
                    if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                        if min_change_percent is not None:
                            denominator = abs(baseline_val) if abs(baseline_val) > 0.001 else 1.0
                            relative_change = abs(current_val - baseline_val) / denominator
                            if relative_change < min_change_percent:
                                await asyncio.sleep(0.02)
                                continue
                        else:
                            if abs(current_val - baseline_val) < 0.001:
                                await asyncio.sleep(0.02)
                                continue
                except Exception:
                    pass
                    
                measured_latency = asyncio.get_event_loop().time() - start_time
                change_detected = True
                break
            await asyncio.sleep(0.02)
        
        if change_detected and measured_latency is not None:
            print(f"      [LATENCY CALIBRATION]{run_label} SUCCESS: Measured latency = {measured_latency:.3f}s")
            latencies.append(measured_latency)
        else:
            print(f"      [LATENCY CALIBRATION]{run_label} ERROR: Calibration timed out! No sensor change detected within {timeout}s.")
    
    if not hasattr(adapter, "_calibration_results"):
        adapter._calibration_results = []

    if latencies:
        max_measured = max(latencies)
        calculated_wait = (max_measured * tolerance_factor) + add_seconds
        if runs > 1:
            print(f"      [LATENCY CALIBRATION] Calibration complete over {runs} runs.")
            print(f"      [LATENCY CALIBRATION] Max measured latency = {max_measured:.3f}s")
        print(f"      [LATENCY CALIBRATION] Calculated wait_dt (with {tolerance_factor}x factor + {add_seconds}s buffer) = {calculated_wait:.3f}s")
        
        # Keep the overall maximum wait time across multiple measure_latency calls!
        if getattr(adapter, "_measured_latency", None) is None:
            adapter._measured_latency = calculated_wait
        else:
            adapter._measured_latency = max(adapter._measured_latency, calculated_wait)

        adapter._calibration_results.append({
            "actuator": f"{actuator} ({actuator_feature})",
            "sensor": f"{sensor} ({sensor_feature})",
            "status": "success",
            "latency": calculated_wait
        })
    else:
        print(f"      [LATENCY CALIBRATION] ERROR: All calibration runs timed out.")
        import warnings
        warnings.warn(
            f"Latency calibration timed out for actuator '{actuator}' and sensor '{sensor}'!",
            UserWarning
        )
        if getattr(adapter, "_measured_latency", None) is None:
            print(f"      [LATENCY CALIBRATION] Using default/fallback wait time.")
            adapter._measured_latency = None
        else:
            print(f"      [LATENCY CALIBRATION] Retaining previously measured maximum wait time of {adapter._measured_latency:.3f}s.")
            
        adapter._calibration_results.append({
            "actuator": f"{actuator} ({actuator_feature})",
            "sensor": f"{sensor} ({sensor_feature})",
            "status": "timeout"
        })
    
    return adapter._measured_latency
