import serial
import paho.mqtt.client as mqtt
import json
import time

PORT = "/dev/ttyACM0"  # Gegebenenfalls auf /dev/ttyUSB0 anpassen, falls nötig
client = mqtt.Client("mein_arduino_client")

# Verbinde mit dem Mosquitto Broker auf dem Raspberry Pi
print("Verbinde mit MQTT-Broker auf 127.0.0.1...")
client.connect("127.0.0.1", 1883)

# 1. Konfiguration & Auto-Discovery an Home Assistant für alle 3 Sensoren
print("Sende Auto-Discovery Konfigurationen an Home Assistant...")
client.publish("homeassistant/sensor/arduino_light/config", json.dumps({
    "name": "Arbeitsplatz Helligkeit",
    "state_topic": "homeassistant/sensor/arduino_light/state",
    "unit_of_measurement": "lx",
    "device_class": "illuminance",
    "unique_id": "arduino_ldr_01"
}), retain=True)

client.publish("homeassistant/sensor/arduino_temp/config", json.dumps({
    "name": "Arbeitsplatz Temperatur",
    "state_topic": "homeassistant/sensor/arduino_temp/state",
    "unit_of_measurement": "°C",
    "device_class": "temperature",
    "unique_id": "arduino_dht11_temp"
}), retain=True)

client.publish("homeassistant/sensor/arduino_hum/config", json.dumps({
    "name": "Arbeitsplatz Luftfeuchtigkeit",
    "state_topic": "homeassistant/sensor/arduino_hum/state",
    "unit_of_measurement": "%",
    "device_class": "humidity",
    "unique_id": "arduino_dht11_hum"
}), retain=True)

# 2. Endlos-Schleife: USB Auslesen und an MQTT weitergeben
print("Starte Sensor-Überwachung...")

while True:
    try:
        # Versuche die USB-Verbindung aufzubauen. Schlägt sofort fehl, wenn das Kabel nicht steckt.
        with serial.Serial(PORT, 9600) as ser:
            print(f"✅ Arduino auf {PORT} verbunden! Lese Daten...")
            
            while True:
                # Warten, bis Daten im seriellen Puffer sind
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    # Prüfen ob es sauberes JSON vom Arduino ist
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            data = json.loads(line)
                            print(f"Update -> Licht: {data['light']} lx | Temp: {data['temp']} °C | Feuchte: {data['hum']} %")
                            
                            # Die 3 ausgelesenen Werte auf die einzelnen Topic-Kanäle schieben
                            client.publish("homeassistant/sensor/arduino_light/state", data["light"])
                            client.publish("homeassistant/sensor/arduino_temp/state", data["temp"])
                            client.publish("homeassistant/sensor/arduino_hum/state", data["hum"])
                        except Exception as e:
                            print(f"Warnung: Konnte Zeile nicht json-parsen: {line}")
                            
    except Exception as e:
        # Wird ausgelöst, wenn das USB-Kabel gezogen wird oder der Port blockiert ist
        print(f"❌ Keine Verbindung zum Arduino. Warte 5 Sekunden... (Fehler: {e})")
        time.sleep(5)
