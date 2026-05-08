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
    "unit_of_measurement": "lx",
    "device_class": "illuminance",
    "unique_id": "arduino_ldr_01"
}), retain=True)

client.publish("homeassistant/sensor/arbeitsplatz_helligkeit_2/config", json.dumps({
    "name": "Arbeitsplatz Helligkeit 2",
    "state_topic": "homeassistant/sensor/arbeitsplatz_helligkeit_2/state",
    "unit_of_measurement": "lx",
    "device_class": "illuminance",
    "unique_id": "arduino_ldr_02"
}), retain=True)

client.publish("homeassistant/sensor/arbeitsplatz_temperatur/config", json.dumps({
    "name": "Arbeitsplatz Temperatur",
    "state_topic": "homeassistant/sensor/arbeitsplatz_temperatur/state",
    "unit_of_measurement": "°C",
    "device_class": "temperature",
    "unique_id": "arduino_dht11_temp"
}), retain=True)

client.publish("homeassistant/sensor/arbeitsplatz_luftfeuchtigkeit/config", json.dumps({
    "name": "Arbeitsplatz Luftfeuchtigkeit",
    "state_topic": "homeassistant/sensor/arbeitsplatz_luftfeuchtigkeit/state",
    "unit_of_measurement": "%",
    "device_class": "humidity",
    "unique_id": "arduino_dht11_hum"
}), retain=True)

client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/config", json.dumps({
    "name": "Arbeitsplatz Fernbedienung",
    "state_topic": "homeassistant/sensor/arbeitsplatz_fernbedienung/state",
    "icon": "mdi:remote-tv",
    "unique_id": "arduino_ir_remote"
}), retain=True)

# Übersetzungstabelle für deine schwarze ELEGOO Fernbedienung (Hex -> String)
ELEGOO_MAP = {
    "45": "POWER", "46": "VOL+", "47": "FUNC",
    "44": "PREV", "40": "PLAY", "43": "NEXT",
    "7": "DOWN", "15": "VOL-", "9": "UP",
    "16": "0", "19": "EQ", "13": "ST_REPT",
    "c": "1", "18": "2", "5e": "3",
    "8": "4", "1c": "5", "5a": "6",
    "42": "7", "52": "8", "4a": "9"
}

def reset_ir_sensor():
    # Setzt den Sensor nach 0.5 Sekunden zurück, damit die gleiche Taste doppelt gedrückt werden kann
    client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/state", "idle")

# 2. Endlos-Schleife: USB Auslesen und an MQTT weitergeben
print("Starte Sensor-Überwachung...")

last_press_time = 0

while True:
    try:
        # timeout=1 ist wichtig: readline() wartet bis zu 1 Sekunde auf Daten.
        # Das verhindert die 99% CPU Last (Busy Waiting).
        with serial.Serial(PORT, 9600, timeout=1) as ser:
            print(f"✅ Arduino auf {PORT} verbunden!")
            client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/state", "idle")

            while True:
                # Hier "schläft" das Skript nun effizient, bis der Arduino eine Zeile sendet
                line = ser.readline().decode('utf-8', errors='ignore').strip()

                if not line:
                    continue  # Timeout erreicht, keine Daten da -> weitermachen

                if line.startswith("{") and line.endswith("}"):
                    try:
                        data = json.loads(line)

                        # Fall 1: Infrarot
                        if "ir_btn" in data:
                            current_time = time.time()
                            if current_time - last_press_time > 0.8:
                                last_press_time = current_time
                                hex_val = data["ir_btn"].lower()
                                btn_name = ELEGOO_MAP.get(hex_val, f"UNKNOWN_{hex_val}")

                                print(f"🔘 Taste: {btn_name}")
                                client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/state", btn_name)
                                threading.Timer(0.5, reset_ir_sensor).start()

                        # Fall 2: Sensoren
                        elif "light" in data:
                            print(f"Update -> L1: {data['light']} | L2: {data.get('light2', 'N/A')} | T: {data['temp']} | H: {data['hum']}")
                            client.publish("homeassistant/sensor/arbeitsplatz_helligkeit/state", data["light"])
                            if "light2" in data:
                                client.publish("homeassistant/sensor/arbeitsplatz_helligkeit_2/state", data["light2"])
                            client.publish("homeassistant/sensor/arbeitsplatz_temperatur/state", data["temp"])
                            client.publish("homeassistant/sensor/arbeitsplatz_luftfeuchtigkeit/state", data["hum"])

                    except json.JSONDecodeError:
                        pass  # Kaputtes JSON ignorieren

    except Exception as e:
        print(f"❌ Verbindung verloren oder Fehler: {e}. Neustart in 5s...")
        time.sleep(5)