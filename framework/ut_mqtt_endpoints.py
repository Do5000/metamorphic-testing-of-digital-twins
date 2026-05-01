import requests
from requests.auth import HTTPBasicAuth
from paho.mqtt import client as mqtt
from ut_params import *
from ut_helpers import *
import json
import time
import threading
import uuid
import queue

class ThreadSafeDict:
    def __init__(self):
        self._dict={}
        self._lock=threading.Lock()
    def set(self,key,value):
        with self._lock:self._dict[key]=value
    def get(self,key,default=None):
        with self._lock:return self._dict.get(key,default)
    def remove(self,key):
        with self._lock:del self._dict[key]
    def clear(self):
        with self._lock:self._dict.clear()
    def __contains__(self,key):
        with self._lock:return key in self._dict
    def __iter__(self):
        with self._lock:return iter(self._dict.copy())
    def items(self):
        with self._lock:return list(self._dict.items())
    def __len__(self):
        with self._lock:return len(self._dict)


class EndpointMQTTandHTTP:
    def __init__(self, ip=None, mqtt_port=None, user=None, pw=None, mqtt_topics = None, mqtt_client = None):
        self.ip = ip
        self.mqtt_port = mqtt_port
        self.user = user
        self.pw = pw
        self.mqtt_topics = mqtt_topics
        self.mqtt_client = mqtt_client

        self.on_device_param_updated = lambda device, param, value: print("[MQTT]", "Message:", (device, param, value))


    def try_subscribe(self, topics):
        for topic in topics:
            code, mid = self.mqtt_client.subscribe(topic)
            if code == mqtt.MQTT_ERR_SUCCESS:
                self.set_in_progress.set(mid, topic)
            self.set_retry.set(mid, topic)


    def handle_mqtt_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != mqtt.CONNACK_ACCEPTED:
            print("[MQTT]", "Connection failed:", reason_code)
            return
        print("[MQTT]", "Connection:", reason_code)
        if self.mqtt_topics is not None:
            self.set_in_progress = ThreadSafeDict()
            self.set_retry = ThreadSafeDict()
            self.retries = 50

            def on_subscribe(client, userdata, mid, reason_code_list, granted_qos):
                self.set_in_progress.remove(mid)
                print("[MQTT]", "Subscribed:", mid, reason_code_list, granted_qos, len(self.set_in_progress), len(self.set_retry))
                if reason_code_list[0] == "Granted QoS 0":
                    self.set_retry.remove(mid)
                if len(self.set_in_progress) == 0 and len(self.set_retry) > 0:
                    self.retries -= 1
                    time.sleep(1)
                    if self.retries <= 0:
                        print("[MQTT]", "Failed to subscribe to topics after retries:", list(self.set_retry.items()))
                        return
                    topics = [topic for _, topic in self.set_retry.items()]
                    self.set_retry.clear()
                    self.try_subscribe(topics)
                
            self.mqtt_client.on_subscribe = on_subscribe
            self.try_subscribe(self.mqtt_topics)
            


    def parse_mqtt_message(self, message):
        return (message.topic,  message.topic, message.payload)


    def handle_mqtt_message(self, client, userdata, message):
        self.on_device_param_updated(*self.parse_mqtt_message(message))


    def send_value(self, device, param_values):
        raise NotImplementedError
    
    def create_client(self):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, str(uuid.uuid4()))
    
    def disconnect_mqtt(self):
        if self.mqtt_client is not None:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()

    def is_connected(self):
        return self.mqtt_client is not None and self.mqtt_client.is_connected()

    def connect_mqtt(self):
        self.disconnect_mqtt()
        
        if self.mqtt_client is None:
            self.mqtt_client = self.create_client()

        if self.user is not None:
            self.mqtt_client.username_pw_set(self.user, self.pw)

        self.mqtt_client.on_connect=self.handle_mqtt_connect
        self.mqtt_client.on_message=self.handle_mqtt_message
        self.mqtt_client.connect(self.ip, self.mqtt_port)
        self.mqtt_client.loop_start()


def parse(parser, val, default_val):
    try:
        return parser(val)
    except Exception:
        return default_val
    


class Homeassistant(EndpointMQTTandHTTP):
    def __init__(self):
        super().__init__(HA_IP, HA_MQTT_PORT, HA_USER, HA_PW, ["homeassistant/#"])

    def parse_mqtt_message(self, message):
        parts = message.topic.split('/')
        device = f'{parts[1]}.{parts[2]}'
        param = parts[3]

        return (device, param, message.payload.decode())
    
    def parse_from_hono(self, vals):
        if 'state' in vals:
            vals['state'] = 'on' if parse(int, vals['state'], 0) == 1 else 'off'
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) * 255
        if 'current_position' in vals:
            vals['current_position'] = int(parse(float, vals['current_position'], 0) * 100)
        if 'current_tilt_position' in vals:
            vals['current_tilt_position'] = int(parse(float, vals['current_tilt_position'], 0) * 100)
        return vals

    def parse_to_hono(self, vals):
        if 'state' in vals:
            vals['state'] = 1 if vals['state'] == 'on' else 0
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) / 255.0
        if 'current_position' in vals:
            vals['current_position'] = parse(float, vals['current_position'], 0) / 100.0
        if 'current_tilt_position' in vals:
            vals['current_tilt_position'] = parse(float, vals['current_tilt_position'], 0) / 100.0
        return vals

    def send_value(self, device, param_values):
        param_values = self.parse_from_hono(param_values)
        requests.post(
            f'http://{HA_HTTP_ADDRESS}/api/states/{device}',
            headers={
                'Authorization':HA_TOKEN,
                'Content-Type':'application/json'},
            json=param_values
        )


class Middleware(EndpointMQTTandHTTP):
    def __init__(self):
        super().__init__(MW_IP, MW_MQTT_PORT, MW_USER, MW_PW, ["middleware/+/#"])

    def parse_mqtt_message(self, message):
        parts = message.topic.split('/')
        device = parts[1]
        param = parts[2]

        return (device, param, message.payload.decode())
    
    def parse_from_hono(self, vals):
        if 'state' in vals:
            vals['state'] = 'on' if parse(int, vals['state'], 0) == 1 else 'off'
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) * 255
        if 'current_position' in vals:
            vals['current_position'] = int(parse(float, vals['current_position'], 0) * 100)
        if 'current_tilt_position' in vals:
            vals['current_tilt_position'] = int(parse(float, vals['current_tilt_position'], 0) * 100)
        return vals

    def parse_to_hono(self, vals):
        if 'state' in vals:
            vals['state'] = 1 if vals['state'] == 'on' else 0
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) / 255.0
        if 'current_position' in vals:
            vals['current_position'] = parse(float, vals['current_position'], 0) / 100.0
        if 'current_tilt_position' in vals:
            vals['current_tilt_position'] = parse(float, vals['current_tilt_position'], 0) / 100.0

        return vals

    def send_value(self, device, param_values):
        param_values = self.parse_from_hono(param_values)
        requests.post(
            f"http://{MW_HTTP_ADDRESS}/middleware/command",
            headers={'Content-Type': 'application/json'},
            json={
                "uuid": device,
                "parameters": [{'name': key, 'value': value} for key, value in param_values.items()]
            }
        )

class Hono(EndpointMQTTandHTTP):
    def __init__(self):
        super().__init__(HONO_MQTT_IP, HONO_MQTT_PORT, f"{HONO_GATEWAY_NAME}@{UT_TENANT}", HONO_GATEWAY_PW, [f"c/{UT_TENANT}/+/q/#"])
        self.q=queue.Queue()
        self.worker=None
        self.lock=threading.Lock()


    def parse_mqtt_message(self, message):
        parts = message.topic.split('/')
        device = parts[2].split(':')[1]
        param = parts[-1]

        payload = json.loads(message.payload.decode())

        return (device, param, payload.get("value"))
    

    def send_value_mqtt(self, device, param_values):
        if not self.mqtt_client or not self.mqtt_client.is_connected():
            return
        for param, value in param_values.items():
            self.mqtt_client.publish(
                f"telemetry/{UT_TENANT}/{UT_TENANT}:{device}",
                json.dumps({
                    "topic":f"{UT_TENANT}/{device}/things/twin/commands/modify",
                    "path":f"/features/{param}/properties/value",
                    "value":value
                })
            )



    def send_value(self, device, param_values):
        for param, value in param_values.items():
        #     self.q.put((device, param, value))
        # with self.lock:
        #     if not self.worker or not self.worker.is_alive():
        #         self.worker = threading.Thread(target=self._worker, daemon=True)
        #         self.worker.start()
            requests.post(
                f"https://{HONO_HTTP_IP}:8443/telemetry",
                headers={'Content-Type':'application/json'},
                data=json.dumps({
                    "topic":f"{UT_TENANT}/{device}/things/twin/commands/modify",
                    "path":f"/features/{param}/properties/value",
                    "value":value
                }),
                auth=HTTPBasicAuth(f"{device}@{UT_TENANT}", DEVICE_PW),
                verify=False
            )



    def create_client(self):
        client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, str(uuid.uuid4()))
        client.tls_set(cert_reqs=mqtt.ssl.CERT_NONE)
        return client