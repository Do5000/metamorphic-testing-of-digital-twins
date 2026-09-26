import serial
import paho.mqtt.client as mqtt
import json
import time
import threading

import os

# Versuche den passenden Port automatisch zu finden (Mac oder Linux)
def find_arduino_port():
    ports = ["/dev/ttyACM0", "/dev/ttyUSB0"] # Linux
    # Suche auf Mac nach usbmodem oder usbserial
    if os.path.exists("/dev"):
        for p in os.listdir("/dev"):
            if "usbmodem" in p or "usbserial" in p:
                ports.append(os.path.join("/dev", p))

    for port in ports:
        if os.path.exists(port):
            return port
    return "/dev/ttyACM0" # Fallback

PORT = find_arduino_port()
print(f"Benutze Port: {PORT}")

try:
    # Für paho-mqtt >= 2.0
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "mein_arduino_client")
except AttributeError:
    # Für ältere paho-mqtt Versionen (< 2.0)
    client = mqtt.Client("mein_arduino_client")

# Verbinde mit dem Mosquitto Broker auf dem Raspberry Pi
print("Verbinde mit MQTT-Broker auf 192.168.8.30...")
client.username_pw_set("mqtt_user", "mqtt_password")
client.connect("192.168.8.30", 1883)
client.loop_start()  # WICHTIG: Startet den Netzwerk-Loop im Hintergrund

# 1. Konfiguration & Auto-Discovery an Home Assistant für alle 3 Sensoren + IR Fernbedienung
print("Sende Auto-Discovery Konfigurationen an Home Assistant...")
client.publish("homeassistant/sensor/arbeitsplatz_helligkeit/config", json.dumps({
    "name": "Arbeitsplatz Helligkeit",
    "state_topic": "homeassistant/sensor/arbeitsplatz_helligkeit/state",
    "unit_of_measurement": "V",
    "device_class": "voltage",
    "state_class": "measurement",
    "suggested_display_precision": 2,
    "unique_id": "arduino_ldr_01"
}), retain=True)

client.publish("homeassistant/binary_sensor/arbeitsplatz_praesenz/config", json.dumps({
    "name": "Arbeitsplatz Präsenz",
    "state_topic": "homeassistant/binary_sensor/arbeitsplatz_praesenz/state",
    "device_class": "occupancy",
    "payload_on": "ON",
    "payload_off": "OFF",
    "unique_id": "arduino_pir_am312"
}), retain=True)

# 2. Endlos-Schleife: USB Auslesen und an MQTT weitergeben
print("Starte Sensor-Überwachung...")

last_press_time = 0

while True:
    try:
        # timeout=1 ist wichtig: readline() wartet bis zu 1 Sekunde auf Daten.
        # Das verhindert die 99% CPU Last (Busy Waiting).
        with serial.Serial(PORT, 9600, timeout=1) as ser:
            print(f"✅ Arduino auf {PORT} verbunden!")

            while True:
                # Hier "schläft" das Skript nun effizient, bis der Arduino eine Zeile sendet
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if not line:
                    continue  # Timeout erreicht, keine Daten da -> weitermachen

                if line.startswith("{") and line.endswith("}"):
                    try:
                        data = json.loads(line)

                        # Fall 1: Präsenz (PIR)
                        if "pir" in data:
                            print(f"Update -> PIR: {data['pir']}")
                            state_str = "ON" if data["pir"] == 1 else "OFF"
                            client.publish("homeassistant/binary_sensor/arbeitsplatz_praesenz/state", state_str, retain=True)

                        # Fall 2: Helligkeitssensor
                        elif "light" in data:
                            print(f"Update -> L1: {data['light']}")
                            client.publish("homeassistant/sensor/arbeitsplatz_helligkeit/state", data["light"], retain=True)

                    except json.JSONDecodeError:
                        pass  # Kaputtes JSON ignorieren

    except Exception as e:
        print(f"❌ Verbindung verloren oder Fehler: {e}. Neustart in 5s...")
        time.sleep(5)