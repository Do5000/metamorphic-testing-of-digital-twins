from ut_mqtt_endpoints import Middleware
from ut_ditto_mock import DittoWebSocket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,Event
import logging
logging.getLogger("werkzeug").setLevel(logging.ERROR)

executor1 = ThreadPoolExecutor(max_workers=1)
middleware = Middleware()
ditto_mock = DittoWebSocket("0.0.0.0", 8082)

import time

# Speicher für die zuletzt gesendeten Befehle und deren Zeitstempel
command_timestamps = {}

def send_with_logging(device, param_val):
    print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] 🚀 START Senden an Middleware: {device} -> {param_val}")
    middleware.send_value(device, param_val)
    print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] ✅ DONE Senden an Middleware: {device} -> {param_val}")

def ditto_mock_on_message(device, param, value):
    if value is not None and param != "errors-response":
        # Befehl speichern, um Echo-Schleifen zu verhindern
        if device not in command_timestamps:
            command_timestamps[device] = {}
        command_timestamps[device][param] = (value, time.time())
        
        print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] 📥 Befehl von Ditto empfangen: {device} -> {param}={value} (Lege in Queue...)")
        executor1.submit(send_with_logging, device, {param:value})
    else:
        print(f"Info (Hono:{device}):", param, value)

def middleware_on_device_param_updated(device, param, value):
    param_val = middleware.parse_to_hono({param:value})
    hono_param, hono_value = list(param_val.items())[0]
    
    # ECHO LOOP FILTER:
    if device in command_timestamps and hono_param in command_timestamps[device]:
        cmd_val, cmd_time = command_timestamps[device][hono_param]
        if cmd_val != hono_value and (time.time() - cmd_time) < 25.0:
            print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] 🛑 Blockiere Echo-Loop: Ignoriere physischen Status {device}->{hono_value}, da wir kürzlich {cmd_val} befohlen haben!")
            return
            
    if hono_value is not None:
        ditto_mock.set_feature(device, hono_param, hono_value)
    else:
        print("Info:", param_val)

def run_ditto_mock_http_endpoint(app):
    app.run(host="0.0.0.0", port=8083, debug=False)

def main():
    ditto_mock.on_command = ditto_mock_on_message
    middleware.on_device_param_updated = middleware_on_device_param_updated
    app = ditto_mock.create_flask_app()
    Thread(target=run_ditto_mock_http_endpoint, args=(app,), daemon=True).start()
    middleware.connect_mqtt()
    ditto_mock.thread.start()
    stop = Event()
    try:
        stop.wait()
    finally:
        executor1.shutdown(wait=True)
        ditto_mock.disconnect()
        middleware.disconnect_mqtt()

if __name__ == "__main__":
    main()