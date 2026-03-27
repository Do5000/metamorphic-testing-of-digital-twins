from ut_mqtt_endpoints import Middleware
from threading import Event

middleware = Middleware()

def middleware_on_device_param_updated(device, param, value):
    print("Device received:", device, param, value)

middleware.on_device_param_updated = middleware_on_device_param_updated
middleware.connect_mqtt()

print("Listening for MQTT Messages from the Middleware. Waiting...")
try:
    Event().wait()
except KeyboardInterrupt:
    middleware.disconnect_mqtt()
