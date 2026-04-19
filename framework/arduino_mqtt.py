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

while True:
    try:
        # Versuche die USB-Verbindung aufzubauen. Schlägt sofort fehl, wenn das Kabel nicht steckt.
        with serial.Serial(PORT, 9600) as ser:
            print(f"✅ Arduino auf {PORT} verbunden! Lese Daten...")
            client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/state", "idle") # Initialisierung
            
            last_press_time = 0
            
            while True:
                # Warten, bis Daten im seriellen Puffer sind
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    
                    # Prüfen ob es sauberes JSON vom Arduino ist
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            data = json.loads(line)
                            
                            # Fall 1: Eine Infrarot-Taste wurde gedrückt!
                            if "ir_btn" in data:
                                current_time = time.time()
                                
                                # Wenn der Klick weniger als 0.8 Sekunden her ist -> ignorieren (Anti-Wackel / Daumen-Schutz)
                                if current_time - last_press_time > 0.8:
                                    last_press_time = current_time
                                    
                                    hex_val = data["ir_btn"].lower()
                                    btn_name = ELEGOO_MAP.get(hex_val, f"UNKNOWN_{hex_val}")
                                    print(f"🔘 Taste gedrückt: {btn_name} (Code: {hex_val})")
                                    
                                    client.publish("homeassistant/sensor/arbeitsplatz_fernbedienung/state", btn_name)
                                    # Starte Thread, der den Zustand nach 0.5 Sekunden in HA zurücksetzt
                                    threading.Timer(0.5, reset_ir_sensor).start()
                                else:
                                    pass # Daumen drückt immer noch auf die gleiche Taste, wir reagieren nicht!

                            # Fall 2: Sensordaten (Helligkeit/Temp/Humidity)
                            elif "light" in data:
                                print(f"Update -> Licht: {data['light']} lx | Temp: {data['temp']} °C | Feuchte: {data['hum']} %")
                                client.publish("homeassistant/sensor/arbeitsplatz_helligkeit/state", data["light"])
                                client.publish("homeassistant/sensor/arbeitsplatz_temperatur/state", data["temp"])
                                client.publish("homeassistant/sensor/arbeitsplatz_luftfeuchtigkeit/state", data["hum"])
                                
                        except Exception as e:
                            print(f"Warnung: Konnte Zeile nicht json-parsen: {line}. Fehler: {e}")
                            
    except Exception as e:
        # Wird ausgelöst, wenn das USB-Kabel gezogen wird oder der Port blockiert ist
        print(f"❌ Keine Verbindung zum Arduino. Warte 5 Sekunden... (Fehler: {e})")
        time.sleep(5)
