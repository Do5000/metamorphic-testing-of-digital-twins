from ut_mqtt_endpoints import Middleware, Hono
from concurrent.futures import ThreadPoolExecutor
from threading import Event

executor1 = ThreadPoolExecutor(max_workers=10)
executor2 = ThreadPoolExecutor(max_workers=10)
middleware = Middleware()
hono = Hono()

def hono_on_command_received(device,param,value):
    if value is not None and param != "errors-response":
        executor1.submit(middleware.send_value, device, {param:value})
    else:
        print(f"Info (Hono:{device}):", param, value)

def middleware_on_device_param_updated(device, param, value):
    param_val=middleware.parse_to_hono({param:value})
    if param_val[param] is not None:
        executor2.submit(hono.send_value_mqtt, device, param_val)
    else:
        print(f"Info (MW:{device}):", param_val)

def main():
    hono.on_device_param_updated = hono_on_command_received
    middleware.on_device_param_updated = middleware_on_device_param_updated
    hono.connect_mqtt()
    middleware.connect_mqtt()
    stop = Event()
    try:
        stop.wait()
    finally:
        executor1.shutdown(wait=True)
        executor2.shutdown(wait=True)
        hono.disconnect_mqtt()
        middleware.disconnect_mqtt()

if __name__ == "__main__":
    main()