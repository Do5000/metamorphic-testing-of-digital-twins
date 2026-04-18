from ut_ditto_mock_reacting import ReactingDittoWebSocket
from threading import Thread,Event
import logging

logging.getLogger("werkzeug").setLevel(logging.ERROR)

ditto_mock=ReactingDittoWebSocket("0.0.0.0", 8082)

def ditto_mock_on_message(device, param, value):
    print(f"Info (Hono:{device}):", param, value)
    if value is not None and param != "errors-response":
        ditto_mock.set_feature(device, param, value)

def run_ditto_mock_http_endpoint(app):
    app.run(host="0.0.0.0", port=8083)

def main():
    ditto_mock.on_command = ditto_mock_on_message
    app = ditto_mock.create_flask_app()
    Thread(target=run_ditto_mock_http_endpoint, args=(app,), daemon=True).start()
    ditto_mock.thread.start()
    stop = Event()
    stop.wait()
    ditto_mock.disconnect()

if __name__ == "__main__":
    main()

