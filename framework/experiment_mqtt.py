import paho.mqtt.client as mqtt
import time
import json
import threading

messages = []
start_time = time.time()

def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe("middleware/#")
    client.subscribe("telemetry/#")
    client.subscribe("homeassistant/#")

def on_message(client, userdata, msg):
    elapsed = time.time() - start_time
    messages.append(f"[{elapsed:.2f}s] {msg.topic}: {msg.payload.decode('utf-8')}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("twinlight", "twinlight")
client.on_connect = on_connect
client.on_message = on_message

client.connect("138.232.83.30", 1884, 60)
client.loop_start()

time.sleep(2)

print("Starting recording... waiting 120 seconds")
time.sleep(120)

client.loop_stop()
client.disconnect()

with open("mqtt_experiment_log2.txt", "w") as f:
    f.write("\n".join(messages))
