import asyncio
import time
import inspect
import json
from typing import Dict, Any, List, Tuple, Callable

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
        m = LiveValueMonitor(adapter, s["deviceId"], s["feature"], interval=0.5, verbose=True)
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

    async def execute_hook(self, hook_data: Dict[str, Any]) -> None:
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
                    minChangePercent=stmt.get("minChangePercent", 0.1),
                    toleranceFactor=stmt.get("toleranceFactor", 1.2),
                    addSeconds=stmt.get("addSeconds", 0.0),
                    timeout=stmt.get("timeout", 5.0),
                    runs=stmt.get("runs", 3)
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

    async def _handle_invariance_reset(self, actuators: List[Dict[str, str]], intermediateActions: List[Any], sensors: List[Dict[str, str]], verbose: bool, manual_waitTime: Any, wait_dt_callable: Callable) -> None:
        for idx, act in enumerate(actuators):
            if intermediateActions:
                init_val = intermediateActions[idx] if idx < len(intermediateActions) else intermediateActions[0]
            else:
                init_val = "off"
            await self.adapter.set_feature_value(act["deviceId"], act["feature"], init_val)
        
        await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)

    async def execute_test(self, test_data: Dict[str, Any], wait_dt_callable: Callable, verbose: bool = False) -> None:
        print(f"\n[DSL] Executing Test: {test_data.get('name')} (Relation: {test_data.get('relation')})")
        
        relation_name = test_data.get("relation")
        if relation_name == "generation":
            await self._execute_generation(test_data, wait_dt_callable, verbose)
            return
            
        actuators = test_data.get("actuators", [])
        sensors = test_data.get("sensors", [])
        sourceActions = test_data.get("sourceActions", [])
        followUpActions = test_data.get("followupActions", [])
        manual_waitTime = test_data.get("waitTime")
        
        # Source Test Case
        await self._apply_actions(actuators, sourceActions)
        await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)
        source_results = await self._read_sensors(sensors)
            
        followup_results = []
        if followUpActions:
            if relation_name == "invariance":
                intermediateActions = test_data.get("intermediateActions", [])
                await self._handle_invariance_reset(actuators, intermediateActions, sensors, verbose, manual_waitTime, wait_dt_callable)
            
            # Followup Test Case
            await self._apply_actions(actuators, followUpActions)
            await self._wait_for_latency(sensors, verbose, manual_waitTime, wait_dt_callable)
            followup_results = await self._read_sensors(sensors)
                
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
                
        # Build kwargs dynamically from the DSL config
        kwargs = {"verbose": verbose}
        if test_data.get("tolerance") is not None:
            kwargs["tolerance"] = test_data["tolerance"]
        if test_data.get("duration") is not None:
            kwargs["duration"] = test_data["duration"]
        if test_data.get("profile") is not None:
            kwargs["profile"] = test_data["profile"]
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

    async def _execute_generation(self, test_data: Dict[str, Any], wait_dt_callable: Callable, verbose: bool) -> None:
        actuators = test_data.get("actuators", [])
        sensors = test_data.get("sensors", [])
        output_file = test_data.get("historicalFile", "sensor_profile.json")
        
        if not actuators or not sensors:
            raise ValueError("Generation requires at least 1 actuator and 1 sensor.")
            
        # Find the feature to iterate over (prefer 'brightness' or anything other than 'state')
        actuator = next((a for a in actuators if a["feature"] != "state"), actuators[0])
        
        if test_data.get("brightnessLevels"):
            steps = test_data["brightnessLevels"]
        else:
            steps = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
        
        samples = test_data.get("historicalSamples")
        if samples is None:
            samples = len(steps)
        
        profile = []
        for step_val in steps:
            if step_val == 0:
                await self.adapter.set_feature_value(actuator["deviceId"], "state", "off")
            else:
                await self.adapter.set_feature_value(actuator["deviceId"], "state", "on")
                await self.adapter.set_feature_value(actuator["deviceId"], actuator["feature"], step_val)
                
            async with multi_monitor(self.adapter, sensors, verbose):
                await wait_dt_callable()
                
            entry = {"brightness_cmd": step_val}
            
            if len(sensors) > 0:
                val_old = await self.adapter.get_feature_value(sensors[0]["deviceId"], sensors[0]["feature"])
                entry["old_sensor"] = val_old
            if len(sensors) > 1:
                val_neighbor = await self.adapter.get_feature_value(sensors[1]["deviceId"], sensors[1]["feature"])
                entry["neighbor_sensor"] = val_neighbor
                
            profile.append(entry)
            print(f"      [GENERATION] Step {step_val}/{samples} -> Old: {entry.get('old_sensor')}, Neighbor: {entry.get('neighbor_sensor')}")
            
        profile_data = {
            "actuator_id": actuator["deviceId"],
            "profile": profile
        }
        
        with open(output_file, "w") as f:
            json.dump(profile_data, f, indent=4)
            
        print(f"      [DSL] Generation Profile saved to {output_file} successfully!")
