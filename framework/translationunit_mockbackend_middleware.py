from ut_mqtt_endpoints import Middleware
from ut_ditto_mock import DittoWebSocket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread,Event
import logging
logging.getLogger("werkzeug").setLevel(logging.ERROR)

executor1 = ThreadPoolExecutor(max_workers=10)
middleware = Middleware()
ditto_mock = DittoWebSocket("0.0.0.0", 8082)

def ditto_mock_on_message(device, param, value):
    if value is not None and param != "errors-response":
        executor1.submit(middleware.send_value, device, {param:value})
    else:
        print(f"Info (Hono:{device}):", param, value)

def middleware_on_device_param_updated(device, param, value):
    param_val = middleware.parse_to_hono({param:value})
    param,value = list(param_val.items())[0]
    if value is not None:
        ditto_mock.set_feature(device, param, value)
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