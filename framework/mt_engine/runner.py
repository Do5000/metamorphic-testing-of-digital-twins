import asyncio
import time
import inspect
import json
from typing import Dict, Any, List, Tuple, Callable, Optional

from pytest_dt_mt.core import DigitalTwinAdapter, PreconditionFailedError
from pytest_dt_mt.relations.base import MetamorphicRelationError
from pytest_dt_mt.relations import get_relation_class
from pytest_dt_mt.monitoring import LiveValueMonitor
from contextlib import asynccontextmanager

@asynccontextmanager
async def multi_monitor(adapter: DigitalTwinAdapter, sensors: List[Dict[str, str]], verbose: bool):
    if not verbose or not sensors:
        yield
        return
        
    monitors = []
    for s in sensors:
        m = LiveValueMonitor(adapter, s["deviceId"], s["feature"], verbose=True)
        monitors.append(m)
        
    for m in monitors:
        await m.__aenter__()
        
    try:
        yield
    finally:
        for m in monitors:
            await m.__aexit__(None, None, None)

class DslRunner:
    def __init__(self, adapter: DigitalTwinAdapter, config: Dict[Any, Any]):
        self.adapter = adapter
        self.config = config

    async def execute_hook(self, hook_data: Dict[str, Any], wait_time: Optional[float] = None) -> None:
        print(f"\n[DSL] Executing hook: {hook_data.get('hookType')}")
        statements = hook_data.get("statements", [])
        for stmt in statements:
            if stmt["type"] == "SetFeature":
                await self.adapter.set_feature_value(stmt["actuator"], stmt["feature"], stmt["value"])
            elif stmt["type"] == "RequirePrecondition":
                await self.adapter.require_precondition(
                    stmt["sensor"], stmt["feature"], stmt["value"], stmt.get("skipMessage")
                )
            elif stmt["type"] == "MeasureLatency":
                kwargs = {k: v for k, v in stmt.items() if k != "type" and v is not None}
                await self.adapter.measure_latency(
                    actuator=stmt["actuator"],
                    actuatorFeature=stmt.get("actuatorFeature", "state"),
                    sensor=stmt["sensor"],
                    sensorFeature=stmt.get("sensorFeature", "state"),
                    valOff=stmt["valOff"],
                    valOn=stmt["valOn"],
                    minChangePercent=stmt.get("minChangePercent"),
                    maxSettleTolerance=stmt.get("maxSettleTolerance"),
                    toleranceFactor=stmt.get("toleranceFactor"),
                    addSeconds=stmt.get("addSeconds"),
                    timeout=stmt.get("timeout"),
                    runs=stmt.get("runs"),
                    settleTime=stmt.get("settleTime"),
                    waitTime=wait_time
                )

    async def _apply_actions(self, actuators: List[Dict[str, str]], actions: List[Any]) -> None:
        for idx, act in enumerate(actuators):
            val = actions[idx] if idx < len(actions) else actions[0]
            await self.adapter.set_feature_value(act["deviceId"], act["feature"], val)

    async def _wait_for_latency(self, sensors: List[Dict[str, str]], verbose: bool, manual_waitTime: Any, wait_dt_callable: Callable) -> None:
        async with multi_monitor(self.adapter, sensors, verbose):
            if manual_waitTime is not None:
                await asyncio.sleep(manual_waitTime)
            else:
                await wait_dt_callable()

    async def _read_sensors(self, sensors: List[Dict[str, str]]) -> List[Any]:
        results = []
        for s in sensors:
            val = await self.adapter.get_feature_value(s["deviceId"], s["feature"])
            results.append(val)
        return results

    async def _handle_invariance_reset(self, actuators: List[Dict[str, str]], intermediateActions: List[Any], sensors: List[Dict[str, str]], verbose: bool, manual_waitTime: Any, wait_dt_callable: Callable) -> List[Any]:
        for idx, act in enumerate(actuators):
            if intermediateActions:
                init_val = intermediateActions[idx] if idx < len(intermediateActions) else intermediateActions[0]
            else:
                init_val = "off"
            await self.adapter.set_feature_value(act["deviceId"], act["feature"], init_val)
        
        await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)
        return await self._read_sensors(sensors)

    async def execute_test(self, test_data: Dict[str, Any], wait_dt_callable: Callable, verbose: bool = False) -> None:
        print(f"\n[DSL] Executing Test: {test_data.get('name')} (Relation: {test_data.get('relation')})")
        
        relation_name = test_data.get("relation")
        actuators = test_data.get("actuators", [])
        sensors = test_data.get("sensors", [])
        sourceActions = test_data.get("sourceActions", [])
        followUpActions = test_data.get("followupActions", [])
        manual_waitTime = test_data.get("waitTime")
        
        # Source Test Case
        await self._apply_actions(actuators, sourceActions)
        await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)
        source_results = await self._read_sensors(sensors)
        for idx, val in enumerate(source_results):
            if val is None:
                s_info = sensors[idx] if idx < len(sensors) else {"deviceId": "unknown", "feature": "unknown"}
                raise AssertionError(f"Sensor '{s_info.get('deviceId')}' ({s_info.get('feature')}) returned None during source test case (device offline or feature not found in Digital Twin).")
            
        followup_results = []
        intermediate_results = []
        if followUpActions:
            if relation_name == "invariance":
                intermediateActions = test_data.get("intermediateActions", [])
                intermediate_results = await self._handle_invariance_reset(actuators, intermediateActions, sensors, verbose, manual_waitTime, wait_dt_callable)
                for idx, val in enumerate(intermediate_results):
                    if val is None:
                        s_info = sensors[idx] if idx < len(sensors) else {"deviceId": "unknown", "feature": "unknown"}
                        raise AssertionError(f"Sensor '{s_info.get('deviceId')}' ({s_info.get('feature')}) returned None during intermediate reset (device offline or feature not found in Digital Twin).")
            
            # Followup Test Case
            await self._apply_actions(actuators, followUpActions)
            await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)
            followup_results = await self._read_sensors(sensors)
            for idx, val in enumerate(followup_results):
                if val is None:
                    s_info = sensors[idx] if idx < len(sensors) else {"deviceId": "unknown", "feature": "unknown"}
                    raise AssertionError(f"Sensor '{s_info.get('deviceId')}' ({s_info.get('feature')}) returned None during follow-up test case (device offline or feature not found in Digital Twin).")
                
        # Run Relation
        relation_class = get_relation_class(relation_name)
            
        eval_result = []
        max_len = max(len(source_results), len(followup_results)) if followup_results else len(source_results)
        
        if relation_name == "stability":
            eval_result = [sensors[0]["deviceId"], sensors[0]["feature"]]
        else:
            for i in range(max_len):
                if i < len(source_results):
                    eval_result.append(source_results[i])
                if i < len(followup_results):
                    eval_result.append(followup_results[i])
                if relation_name == "invariance" and i < len(intermediate_results):
                    eval_result.append(intermediate_results[i])
                
        # Build kwargs dynamically from the DSL config
        kwargs = {"verbose": verbose}
        if test_data.get("tolerance") is not None:
            kwargs["tolerance"] = test_data["tolerance"]
        if test_data.get("duration") is not None:
            kwargs["duration"] = test_data["duration"]
        if test_data.get("not") is not None:
            kwargs["not"] = test_data["not"]
            
        relation_instance = relation_class(**kwargs)
        is_inverted = kwargs.get("not", False)
        original_failed = False
        original_error = None

        try:
            if inspect.iscoroutinefunction(relation_instance.evaluate):
                await relation_instance.evaluate(eval_result, dt_adapter=self.adapter)
            else:
                relation_instance.evaluate(eval_result, dt_adapter=self.adapter)
        except MetamorphicRelationError as e:
            original_failed = True
            original_error = e

        if is_inverted:
            if original_failed:
                print(f"      [DSL] Inverted {relation_name} Relation Passed successfully! (Original failed as expected: {original_error})")
            else:
                msg = f"Metamorphic Relation ({relation_name}) expected to fail but passed."
                print(f"      [DSL] {msg}")
                raise MetamorphicRelationError(msg)
        else:
            if original_failed:
                print(f"      [DSL] Metamorphic Relation ({relation_name}) failed: {original_error}")
                raise original_error
            else:
                print(f"      [DSL] {relation_name} Relation Passed successfully!")
