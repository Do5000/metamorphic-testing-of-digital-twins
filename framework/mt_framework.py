import asyncio
import httpx
from ut_helpers import UT_TENANT, DITTO_USER, DITTO_PW

import websockets
import json

class DigitalTwinAdapter:
    """
    Adapter to interface with the Digital Twin backend (Ditto).
    Uses WebSockets for real-time commands and HTTP for state retrieval.
    """
    def __init__(self, http_url="http://127.0.0.1:8083", ws_url="ws://127.0.0.1:8082/ws/2"):
        self.http_url = http_url
        self.ws_url = ws_url
        self._ws = None

    async def _get_ws(self):
        from websockets.protocol import State
        
        if self._ws is None or self._ws.state is not State.OPEN:
            # We add ping_interval and ping_timeout to keep the connection alive
            # during the wait periods.
            self._ws = await websockets.connect(
                self.ws_url,
                ping_interval=20,  # Send a ping every 20 seconds
                ping_timeout=20    # Wait 20 seconds for a pong response
            )
        return self._ws

    async def close(self):
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def get_state(self, device_id):
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(
                f'{self.http_url}/api/2/things/{UT_TENANT}:{device_id}',
                auth=(DITTO_USER, DITTO_PW)
            )
            return resp.json()
        
    async def get_feature_value(self, device_id, feature_name):
        device = await self.get_state(device_id)
        if 'features' in device and feature_name in device['features']:
            return device['features'][feature_name]['properties']['value']
        return None

    async def set_feature_value(self, device_id, feature_name, value):
        """
        Sends a command via WebSocket
        """
        ws = await self._get_ws()
        msg = {
            "topic": f"{UT_TENANT}/{device_id}/things/live/messages/{feature_name}",
            "headers": {
                "content-type": "application/json",
                "response-required": False
            },
            "path": f"/inbox/messages/{feature_name}",
            "value": value
        }
        await ws.send(json.dumps(msg))
        return 200 # Success status code

class LiveValueMonitor:
    """
    Background worker that polls a sensor value and logs it during the test.
    Helps identify timing issues or signal noise.
    """
    def __init__(self, adapter, device_id, feature_name, interval=1.0):
        self.adapter = adapter
        self.device_id = device_id
        self.feature_name = feature_name
        self.interval = interval
        self.history = []
        self._stop_event = asyncio.Event()
        self._task = None

    async def _run(self):
        start_time = asyncio.get_event_loop().time()
        while not self._stop_event.is_set():
            val = await self.adapter.get_feature_value(self.device_id, self.feature_name)
            elapsed = asyncio.get_event_loop().time() - start_time
            self.history.append((elapsed, val))
            # Optional: Live printing of progression
            print(f"      [LIVE MONITOR] {self.device_id} @ {elapsed:4.1f}s: {val}")
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                continue

    async def __aenter__(self):
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        if self._task:
            await self._task

class MetamorphicRelation:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    async def execute(self, dt_adapter, test_config):
        raise NotImplementedError("Subclasses must implement execute()")

class MonotonicityRelation(MetamorphicRelation):
    def __init__(self):
        super().__init__("Monotonicity", "If I increase the actuator input, the sensor output must not decrease.")
        
    async def execute(self, dt_adapter, test_config):
        """
        Expects test_config defining actuator setup and sensor to evaluate.
        """
        a_id = test_config['actuator_id']
        a_feat = test_config['actuator_feature']
        s_id = test_config['sensor_id']
        s_feat = test_config['sensor_feature']
        
        # --- Source Test Case ---
        await dt_adapter.set_feature_value(a_id, a_feat, test_config['initial_input'])
        
        if test_config.get('wait_time'):
            if test_config.get('monitor_live'):
                async with LiveValueMonitor(dt_adapter, s_id, s_feat):
                    await asyncio.sleep(test_config['wait_time'])
            else:
                await asyncio.sleep(test_config['wait_time'])
        
        source_output = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Monotonicity] Source output ({s_id}.{s_feat}): {source_output}")
        
        # --- Follow-up Test Case ---
        await dt_adapter.set_feature_value(a_id, a_feat, test_config['increased_input'])
        
        if test_config.get('wait_time'):
            if test_config.get('monitor_live'):
                async with LiveValueMonitor(dt_adapter, s_id, s_feat):
                    await asyncio.sleep(test_config['wait_time'])
            else:
                await asyncio.sleep(test_config['wait_time'])
        
        followup_output = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Monotonicity] Follow-up output ({s_id}.{s_feat}): {followup_output}")
        
        if source_output is None or followup_output is None:
            return False, f"Missing output. Source: {source_output}, Followup: {followup_output}"

        # Attempt to convert to float for proper numeric comparison
        try:
            s_val = float(source_output)
            f_val = float(followup_output)
            passed = f_val >= s_val
            msg = f"Output: {s_val} -> {f_val} (Valid: >=)" if passed else f"Output decreased! {f_val} < {s_val}"
        except (ValueError, TypeError):
            # Fallback to string comparison if not numeric
            passed = followup_output >= source_output
            msg = f"Output (str): {source_output} -> {followup_output} (Valid: >=)" if passed else f"Output decreased (str)! {followup_output} < {source_output}"
            
        return passed, msg

class InvarianceRelation(MetamorphicRelation):
    def __init__(self):
        super().__init__("Invariance", "Under stable conditions, the same input should lead to the same output.")
        
    async def execute(self, dt_adapter, test_config):
        a_id = test_config['actuator_id']
        a_feat = test_config['actuator_feature']
        s_id = test_config['sensor_id']
        s_feat = test_config['sensor_feature']
        
        # --- Evaluation 1 ---
        await dt_adapter.set_feature_value(a_id, a_feat, test_config['input_value'])
        if test_config.get('wait_time'): await asyncio.sleep(test_config['wait_time'])
        out1 = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Invariance] Output 1 ({s_id}.{s_feat}): {out1}")
        
        # Interference / Reset step before evaluating again
        await dt_adapter.set_feature_value(a_id, a_feat, test_config.get('reset_value', 0))
        if test_config.get('wait_time'): await asyncio.sleep(test_config['wait_time'])
        
        # --- Evaluation 2 ---
        await dt_adapter.set_feature_value(a_id, a_feat, test_config['input_value'])
        if test_config.get('wait_time'): await asyncio.sleep(test_config['wait_time'])
        out2 = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Invariance] Output 2 ({s_id}.{s_feat}): {out2}")
        
        if out1 is None or out2 is None:
            return False, f"Missing output. Out1: {out1}, Out2: {out2}"
            
        # Attempt to convert to float for proper numeric comparison
        try:
            val1 = float(out1)
            val2 = float(out2)
            tolerance = test_config.get('tolerance', 0.05)
            diff = abs(val1 - val2)
            max_allowed = max(max(val1, val2), 1) * tolerance
            passed = diff <= max_allowed
            msg = f"Outputs Match! ({val1} vs {val2}, Diff {diff} <= allowed {max_allowed})" if passed else f"Outputs differ beyond tolerance: {val1} vs {val2}"
        except (ValueError, TypeError):
            # Fallback for non-numeric
            passed = out1 == out2
            msg = f"Outputs Match (str)! ({out1} vs {out2})" if passed else f"Outputs differ (str): {out1} vs {out2}"
            
        return passed, msg

class ConservationRelation(MetamorphicRelation):
    def __init__(self):
        super().__init__("Conservation", "If inputs are changed keeping total energy equal, overall output remains comparable.")
        
    async def execute(self, dt_adapter, test_config):
        a1_id = test_config['actuator_1_id']
        a2_id = test_config['actuator_2_id']
        feat = test_config['feature']
        s_id = test_config['sensor_id']
        s_feat = test_config['sensor_feature']
        delta = test_config['delta']
        
        # --- Source Test Case ---
        await dt_adapter.set_feature_value(a1_id, feat, test_config['initial_a'])
        await dt_adapter.set_feature_value(a2_id, feat, test_config['initial_b'])
        if test_config.get('wait_time'): await asyncio.sleep(test_config['wait_time'])
        
        source_out = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Conservation] Source output ({s_id}.{s_feat}): {source_out}")
        
        # --- Follow-up Test Case ---
        await dt_adapter.set_feature_value(a1_id, feat, test_config['initial_a'] - delta)
        await dt_adapter.set_feature_value(a2_id, feat, test_config['initial_b'] + delta)
        if test_config.get('wait_time'): await asyncio.sleep(test_config['wait_time'])
        
        followup_out = await dt_adapter.get_feature_value(s_id, s_feat)
        print(f"    [DEBUG Conservation] Follow-up output ({s_id}.{s_feat}): {followup_out}")
        
        if source_out is None or followup_out is None:
            return False, f"Missing output. Source: {source_out}, Followup: {followup_out}"
            
        # Attempt to convert to float for proper numeric comparison
        try:
            s_val = float(source_out)
            f_val = float(followup_out)
            tolerance = test_config.get('tolerance', 0.10)
            diff = abs(s_val - f_val)
            max_allowed = max(max(s_val, f_val), 1) * tolerance
            passed = diff <= max_allowed
            msg = f"Conservation maintained! (Source: {s_val}, Follow-up: {f_val}, Diff: {diff} <= {max_allowed})" if passed else f"Conservation broken: {s_val} vs {f_val}"
        except (ValueError, TypeError):
            passed = source_out == followup_out
            msg = f"Conservation maintained (str)! ({source_out} == {followup_out})" if passed else f"Conservation broken (str): {source_out} vs {followup_out}"

        return passed, msg
