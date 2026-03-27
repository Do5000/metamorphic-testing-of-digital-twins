import hashlib

HONO_MQTT_IP="127.0.0.1"
HONO_MQTT_PORT=8883
HONO_REGISTRY_IP = "127.0.0.1"
HONO_REGISTRY_PORT = 28443
HONO_REGISTRY_ADDRESS = f"{HONO_REGISTRY_IP}:{HONO_REGISTRY_PORT}"
HONO_USER='hono'
HONO_PW='hono-secret'
HONO_HTTP_IP = HONO_REGISTRY_IP
HONO_HTTP_PORT = 8443
HONO_HTTP_ADDRESS = f"{HONO_HTTP_IP}:{HONO_HTTP_PORT}"
HONO_GATEWAY_NAME = 'homeassistantgateway'
HONO_GATEWAY_PW = hashlib.sha256("gatewayPwHomeAssistant".encode()).hexdigest()

UT_TENANT = "at.uibk.ut.tenants"
UT_DEFAULT_DEVICE = "demo-device"
UT_POLICY = f"{UT_TENANT}:{UT_DEFAULT_DEVICE}"

DEVICE_PARAMS = {
    'light': ['brightness', 'state'],
    'blind': ['position'],
    'switch': ['state'],
    'sensor': ['illuminance', 'presence', 'sound_level', 'temperature', 'humidity', 'distance']
}

DEVICES = { # local
    'switch.ac':DEVICE_PARAMS['switch'],
    'switch.decorative_lights':DEVICE_PARAMS['switch'],
    'light.bed_light':DEVICE_PARAMS['light'],
    'light.ceiling_lights':DEVICE_PARAMS['light'],
    'light.kitchen_lights':DEVICE_PARAMS['light'],
    'light.entrance_color_white_lights':DEVICE_PARAMS['light']
}

# DEVICES = { # living-lab
#     'switch.licht_schalter':DEVICE_PARAMS['switch'],
#     'light.sueden_tuer':DEVICE_PARAMS['light'],
#     'light.sueden_fenster':DEVICE_PARAMS['light'],
#     'light.norden_tuer':DEVICE_PARAMS['light'],
#     'light.norden_fenster':DEVICE_PARAMS['light']
# }

DEVICE = "switch.ac"
DEVICE_ID =f"{UT_TENANT}:{DEVICE}"
DEVICE_PW = hashlib.sha256("SuperSecurePW".encode()).hexdigest()

DITTO_NGINX_IP = "127.0.0.1"
DITTO_NGINX_PORT = 8080
DITTO_NGINX_ADDRESS = f"{DITTO_NGINX_IP}:{DITTO_NGINX_PORT}"
DITTO_USER='ditto'
DITTO_PW='ditto'

# HA_IP =  '192.168.1.10' # 'localhost' # local
HA_IP = '138.232.83.30' # living-lab
HA_HTTP_PORT = 8123
HA_HTTP_ADDRESS = f'{HA_IP}:{HA_HTTP_PORT}'
HA_MQTT_PORT = 1885
# HA_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI1MDEzY2MyZjljZjk0NzQ0ODFhNWI5YjFjNTFmNjU1NCIsImlhdCI6MTc0ODg4MDQ3MSwiZXhwIjoyMDY0MjQwNDcxfQ.3NTlw0TmG5mU1OzWoiLgp8Ppj5aTJxrEb4GCxVvP0uE' # local
HA_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwNzI3ZTFhNWE2Y2U0Y2U5OGE1YTU1MGY4Yjg3ZTU5OCIsImlhdCI6MTc0OTIxNTkyNCwiZXhwIjoyMDY0NTc1OTI0fQ.ipWRZ1UKPt5AmzL1mGV2zMSK2ujGbUcKaArBlSn0hn0' # living-lab
HA_USER = 'twinlight'
HA_PW = 'twinlight'

MW_IP = HA_IP
# MW_IP = '192.168.1.10'#'localhost'
MW_USER = 'twinlight'
MW_PW = 'twinlight'
MW_MQTT_PORT = 1884
MW_HTTP_PORT = 8081
MW_HTTP_ADDRESS = f'{MW_IP}:{MW_HTTP_PORT}'