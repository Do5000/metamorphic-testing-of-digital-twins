from datetime import datetime
from ut_params import *
from ut_helpers import *
import asyncio
import threading
import json
import re
import websockets

device_data_initial = {
    # 'switch.ac': {
    # 'attributes': {},
    # 'features': {'state': 1}},

    # 'switch.decorative_light': {
    # 'attributes': {},
    # 'features': {'state': 1}},

    # 'light.bed_light': {
    # 'attributes': {},
    # 'features': {'state': 1, 'brightness': 1}},

    # 'light.ceiling_lights': {
    # 'attributes': {},
    # 'features': {'state': 1, 'brightness': 1}},

    # 'light.entrance_color_white_lights': {
    # 'attributes': {},
    # 'features': {'state': 1, 'brightness': 1}},

    # 'light.norden_tuer': {
    # 'attributes': {},
    # 'features': {'state': 0, 'brightness': 0}},

    # 'light.sueden_tuer': {
    # 'attributes': {},
    # 'features': {'state': 0, 'brightness': 0}},

    # 'light.norden_fenster': {
    # 'attributes': {},
    # 'features': {'state': 0, 'brightness': 0}},

    # 'light.sueden_fenster': {
    # 'attributes': {},
    # 'features': {'state': 0, 'brightness': 0}},

    # 'switch.licht_schalter': {
    # 'attributes': {},
    # 'features': {'state': 0}},

    # 'cover.cover_norden': {
    # 'attributes': {},
    # 'features': {'current_position': 0}},

    # 'cover.cover_sueden': {
    # 'attributes': {},
    # 'features': {'current_position': 0}},
}

MOCK_DEVICE_DATA = {f'{UT_TENANT}:{k}': {
    'thingId': f'{UT_TENANT}:{k}',
    'policyId': 'at.uibk.ut.tenants:demo-device',
    'attributes': v['attributes'],
    'features': {feat_k: {'properties': {'value': feat_v}} for feat_k, feat_v in v['features'].items()}
} for k, v in device_data_initial.items()}


class WebSocketServer:
    def __init__(self, host, port):
        self.uri = f"ws://{host}:{port}"
        self.host = host
        self.port = port
        self.ws = None
        self.on_message = None
        self.loop = asyncio.new_event_loop()
        self.server = None
        self.thread = threading.Thread(target=self._run_loop)

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._start())
        self.loop.run_forever()

    async def _start(self):
        self.server = await websockets.serve(self._handler, self.host, self.port)

    async def _handler(self, ws, path=None):
        if path is None:
            path=getattr(ws, "path", None)
            if path is None: path = ws.request.path
        if path != "/ws/2": 
            await ws.close()
            return
        self.ws = ws
        while True:
            try:
                msg = await ws.recv()
                if self.on_message: self.on_message(msg)
            except: break

    async def _send(self, msg):
        if self.ws: await self.ws.send(msg)

    def send(self, msg):
        asyncio.run_coroutine_threadsafe(self._send(msg), self.loop)

    async def _stop(self):
        if self.server: self.server.close(); await self.server.wait_closed()

    def disconnect(self):
        asyncio.run_coroutine_threadsafe(self._stop(), self.loop).result()
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()




class DittoWebSocket(WebSocketServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.on_message = self.parse_ditto_command
        self.on_command = None
        self.devices = MOCK_DEVICE_DATA
        self.app = None

    def parse_command(self, text):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return None
        topic = data.get("topic", "")
        match = re.match(r'([^/]+)/([^/]+)/things/live/messages/([^/]+)', topic)
        if not match: return None
        ut_tenant, device, command_id = match.groups()
        value = data.get("value")
        return ut_tenant, device, command_id, value

    def parse_ditto_command(self, msg):
        if self.on_command is None: return
        data = self.parse_command(msg)
        if data is None: return

        ut_tenant, device, command_id, value = data
        self.on_command(device, command_id, value)

    def set_attribute(self, device, attribute, value):
        device_id = f'{UT_TENANT}:{device}'
        self.devices[device_id]['attibutes'][attribute] = value
        self.send(json.dumps(
            self._create_modified_message(device, f'/attibutes/{attribute}', value)
        ))

    def _init_feature_if_missing(self, device_id, feature, value):
        #init missing feature
        if feature not in self.devices[device_id]['features']:
            self.devices[device_id]['features'][feature] = {'properties': {'value': value}}

    def _create_mock_device(self, device_id, feature, value):
        #create new mock device
        print(f"Creating new mock device: {device_id} with feature: {feature}")
        self.devices[device_id] = {
            'thingId': device_id,
            'policyId': UT_POLICY,
            'attributes': {},
            'features': {
                feature: {'properties': {'value': value}}
            }
        }

    def set_feature(self, device, feature, value):
        device_id = f'{UT_TENANT}:{device}'
        if device_id not in self.devices:
            # Dynamically create the device if it doesn't exist
            self._create_mock_device(device_id, feature, value)
        self._init_feature_if_missing(device_id, feature, value)
        
        self.devices[device_id]['features'][feature]['properties']['value'] = value
        self.send(json.dumps(
            self._create_modified_message(device, f'/features/{feature}/properties/value', value)
        ))


    def _create_modified_message(self, device, path, value):
        return {
            'topic': f'{UT_TENANT}/{device}/things/twin/events/modified',
            'headers': {'correlation-id': 'c8d33ced-bb6e-4dc2-a1b6-a2f44e95cb3a', # a uuid
            'requested-acks': [],
            'ditto-originator': f'pre-authenticated:hono-connection-{UT_TENANT}',
            'response-required': False,
            'version': 2,
            'content-type': 'application/json'},
            'path': path,
            'value': value,
            'revision': 12513, # running counter
            'timestamp': f'{datetime.now().isoformat()}Z'
        }
    
    def send_value(self, device, param_val):
        for param, val in param_val.items():
            self.send(json.dumps( # DT => PT Websocket update
                self._create_modified_message(device, f'/features/{param}/properties/value', val)
            ))

    def get_device(self, device_id):
        return self.devices.get(device_id, None)
    
    def get_devices(self):
        return list(self.devices.values())
    
    def create_device(self, device_id, policy_id, attributes, features):
        device = {
            'thingId': device_id,
            'policyId': policy_id,
            'attributes': attributes,
            'features': features
        }
        existed = device_id in self.devices
        self.devices[device_id] = device
        return device, existed


    def delete_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False
    

    def create_flask_app(self):
        from flask import Flask, request, jsonify, abort
        self.app = Flask(__name__)

        def _not_found_resp(device_id):
            return jsonify({'status': 404,
                    'error': 'things:thing.notfound',
                    'message': f"The Thing with ID '{device_id}' could not be found or requester had insufficient permissions to access it.",
                    'description': 'Check if the ID of your requested Thing was correct and you have sufficient permissions.'}), 404

        @self.app.route('/api/2/things/<device_id>', methods=['GET'])
        def _get_device(device_id):
            device = self.get_device(device_id)
            if device is None:
                return _not_found_resp(device_id)
            return jsonify(device)
        
        @self.app.route('/api/2/search/things', methods=['GET'])
        def _get_devices():
            devices = self.get_devices()
            options = request.args.get('option')
            options = {option.split('(')[0]:option.split('(')[1][:-1] for option in options.split(',')} if options else {}
            size = int(options.get('size', 200))
            cursor = int(options.get('cursor', 0))
            ret = {'items': devices[cursor:cursor+size]}
            if cursor + size < len(devices):
                ret['cursor'] = str(cursor + size)
            return jsonify(ret)
        
        @self.app.route('/api/2/things/<device_id>', methods=['PUT'])
        def _create_device(device_id):
            data = request.get_json()
            device, existed = self.create_device(device_id=device_id, policy_id=data.get("policyId"), attributes=data.get("attributes", {}), features=data.get("features", {}))
            if not existed:
                return jsonify(device), 201
            return '', 204
        
        @self.app.route('/api/2/things/<device_id>', methods=['DELETE'])
        def _delete_device(device_id):
            if not self.delete_device(device_id):
                return _not_found_resp(device_id)
            return '', 204
        
        @self.app.route('/',defaults={'path': ''}, methods=['GET','POST','PUT','DELETE'])
        @self.app.route('/<path:path>', methods=['GET','POST','PUT','DELETE'])
        def _catch_all(path):
            abort(404)

        
        return self.app


