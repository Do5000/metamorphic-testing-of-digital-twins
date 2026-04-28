import paho.mqtt.client as mqtt
import time

# IP deines Raspberry Pi
BROKER_IP = "192.168.8.30" 

def on_connect(client, userdata, flags, rc, properties=None):
    # Wir abonnieren alles, was nach einer Konfiguration aussieht
    client.subscribe("homeassistant/#")
    print("[*] Suche nach angemeldeten MQTT-Geräten...")

def on_message(client, userdata, msg):
    # Wenn ein Topic auf /config endet, löschen wir es
    if msg.topic.endswith("/config"):
        print(f"[!] Lösche Gerät: {msg.topic}")
        client.publish(msg.topic, payload="", retain=True)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "cleanup_tool")
# Falls dein Raspi eine ältere Paho-Version hat:
# client = mqtt.Client("cleanup_tool")

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, 1883)
client.loop_start()

# Wir lassen das Skript 5 Sekunden laufen, um alle Topics zu finden
time.sleep(5)
client.loop_stop()
print("[*] Bereinigung abgeschlossen.")
