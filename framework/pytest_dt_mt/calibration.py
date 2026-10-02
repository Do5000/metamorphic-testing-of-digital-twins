import asyncio

from . import config

async def measure_latency(
    adapter,
    actuator,
    actuatorFeature,
    valOff,
    valOn,
    sensor,
    sensorFeature,
    toleranceFactor=None,
    addSeconds=None,
    timeout=None,
    minChangePercent=None,
    maxSettleTolerance=None,
    runs=None,
    settleTime=None,
    waitTime=None
):
    toleranceFactor = toleranceFactor if toleranceFactor is not None else config.DEFAULT_TOLERANCE_FACTOR
    addSeconds = addSeconds if addSeconds is not None else config.DEFAULT_ADD_SECONDS
    timeout = timeout if timeout is not None else config.DEFAULT_TIMEOUT
    minChangePercent = minChangePercent if minChangePercent is not None else config.DEFAULT_MIN_CHANGE_PERCENT
    maxSettleTolerance = maxSettleTolerance if maxSettleTolerance is not None else config.DEFAULT_MAX_SETTLE_TOLERANCE
    runs = runs if runs is not None else config.DEFAULT_CALIBRATION_RUNS
    settleTime = settleTime if settleTime is not None else config.DEFAULT_SETTLE_TIME
    waitTime = waitTime if waitTime is not None else config.DEFAULT_CALIBRATION_BASELINE_WAIT

    """
    Dynamically measures the system latency (time from actuator action to sensor response)
    using the Monotony Relation workflow.
    Supports multiple runs and aggregates the maximum calculated wait time across all runs and calls.
    """
    print(f"\n      [LATENCY CALIBRATION] Starting latency calibration...")
    print(f"      [LATENCY CALIBRATION] Actuator: {actuator} ({actuatorFeature})")
    print(f"      [LATENCY CALIBRATION] Sensor: {sensor} ({sensorFeature})")
    if minChangePercent is not None:
        print(f"      [LATENCY CALIBRATION] Minimum change threshold: {minChangePercent * 100:.1f}%")
    if runs > 1:
        print(f"      [LATENCY CALIBRATION] Performing {runs} calibration runs...")
    
    # 1. Ensure WebSocket is connected and background listener task is active
    await adapter._client.get_ws()
    
    latencies = []
    
    for run_idx in range(1, runs + 1):
        run_label = f" (Run {run_idx}/{runs})" if runs > 1 else ""
        
        # 2. Set actuator to off state
        print(f"      [LATENCY CALIBRATION]{run_label} Setting actuator to baseline '{valOff}'...")
        await adapter.set_feature_value(actuator, actuatorFeature, valOff)
        
        # 3. Wait to let the system stabilize and ensure baseline is reached
        await asyncio.sleep(waitTime)
        
        # 4. Get the baseline sensor value and seed the cache
        baseline_val = await adapter.get_feature_value(sensor, sensorFeature, silent=True)
        print(f"      [LATENCY CALIBRATION]{run_label} Baseline sensor value: {baseline_val}")
        
        # 5. Trigger the change: setting actuator to on state
        print(f"      [LATENCY CALIBRATION]{run_label} Triggering change: setting actuator to '{valOn}'...")
        start_time = asyncio.get_event_loop().time()
        await adapter.set_feature_value(actuator, actuatorFeature, valOn)
        
        # 6. Poll cache for change
        change_detected = False
        measured_latency = None
        poll_start = asyncio.get_event_loop().time()
        initial_change_time = None

        
        history = []
        last_poll_time = 0
        
        while asyncio.get_event_loop().time() - poll_start < timeout:
            now = asyncio.get_event_loop().time()
            current_val = adapter._client.cache.get(sensor, {}).get(sensorFeature)
            
            if not change_detected:
                if current_val is not None and current_val != baseline_val:
                    is_significant_change = True
                    try:
                        if isinstance(current_val, (int, float)) and isinstance(baseline_val, (int, float)):
                            if minChangePercent is not None:
                                denominator = abs(baseline_val) if abs(baseline_val) > config.DEFAULT_CALIBRATION_EPSILON else 1.0
                                relative_change = abs(current_val - baseline_val) / denominator
                                if relative_change < minChangePercent:
                                    is_significant_change = False
                            else:
                                if abs(current_val - baseline_val) < config.DEFAULT_CALIBRATION_EPSILON:
                                    is_significant_change = False
                    except Exception:
                        pass
                        
                    if is_significant_change:
                        change_detected = True
                        initial_change_time = now
                        print(f"      [LATENCY CALIBRATION]{run_label} Initial change detected at {now - start_time:.3f}s (value: {current_val})")
                        if settleTime is None:
                            measured_latency = now - start_time
                            break
                        else:
                            history.append((now, current_val))
                            last_poll_time = now
                            print(f"      [LIVE MONITOR] {sensor} @ 0.0s: {current_val}")
            else:
                if current_val != history[-1][1]:
                    history.append((now, current_val))
                
                if now - last_poll_time >= config.DEFAULT_MONITOR_INTERVAL:
                    if history[-1][0] != now:
                        history.append((now, current_val))
                    last_poll_time = now
                    print(f"      [LIVE MONITOR] {sensor} @ {now - initial_change_time:.1f}s: {current_val}")
                
                while len(history) > 1 and now - history[1][0] >= settleTime:
                    history.pop(0)
                
                if now - history[0][0] >= settleTime - config.DEFAULT_CALIBRATION_TIMING_EPSILON:
                    is_stable = True
                    try:
                        vals = [v for t, v in history if isinstance(v, (int, float))]
                        if len(vals) == len(history):
                            min_val = min(vals)
                            max_val = max(vals)
                            if maxSettleTolerance is not None:
                                denominator = abs(min_val) if abs(min_val) > config.DEFAULT_CALIBRATION_EPSILON else 1.0
                                if (max_val - min_val) / denominator > maxSettleTolerance:
                                    is_stable = False
                            else:
                                if max_val - min_val > config.DEFAULT_CALIBRATION_EPSILON:
                                    is_stable = False
                        else:
                            if len(set(v for t, v in history)) > 1:
                                is_stable = False
                    except Exception:
                        if len(set(v for t, v in history)) > 1:
                            is_stable = False
                            
                    if is_stable:
                        settled_time = history[0][0]
                        measured_latency = settled_time - start_time
                        print(f"      [LATENCY CALIBRATION]{run_label} Value settled for {settleTime}s window starting at {measured_latency:.3f}s.")
                        break
            
            await asyncio.sleep(config.DEFAULT_CALIBRATION_POLL_RATE)
        
        if change_detected and measured_latency is not None:
            print(f"      [LATENCY CALIBRATION]{run_label} SUCCESS: Measured latency = {measured_latency:.3f}s")
            latencies.append(measured_latency)
        elif change_detected and measured_latency is None:
            print(f"      [LATENCY CALIBRATION]{run_label} ERROR: Calibration timed out! Sensor changed but did not settle within {timeout}s.")
        else:
            print(f"      [LATENCY CALIBRATION]{run_label} ERROR: Calibration timed out! No sensor change detected within {timeout}s.")
    
    if not hasattr(adapter, "_calibration_results"):
        adapter._calibration_results = []

    if latencies:
        max_measured = max(latencies)
        calculated_wait = (max_measured * toleranceFactor) + addSeconds
        if runs > 1:
            print(f"      [LATENCY CALIBRATION] Calibration complete over {runs} runs.")
            print(f"      [LATENCY CALIBRATION] Max measured latency = {max_measured:.3f}s")
        print(f"      [LATENCY CALIBRATION] Calculated wait_dt (with {toleranceFactor}x factor + {addSeconds}s buffer) = {calculated_wait:.3f}s")
        
        # Keep the overall maximum wait time across multiple measure_latency calls!
        if getattr(adapter, "_measured_latency", None) is None:
            adapter._measured_latency = calculated_wait
        else:
            adapter._measured_latency = max(adapter._measured_latency, calculated_wait)

        adapter._calibration_results.append({
            "actuator": f"{actuator} ({actuatorFeature})",
            "sensor": f"{sensor} ({sensorFeature})",
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
            "actuator": f"{actuator} ({actuatorFeature})",
            "sensor": f"{sensor} ({sensorFeature})",
            "status": "timeout"
        })
    
    return adapter._measured_latency
