import paho.mqtt.client as mqtt
import time

# --- Verbindungsparameter aus deinem Workspace ---
# Entnommen aus ut_params.py
LIVING_LAB_IP = "138.232.83.30"
LIVING_LAB_MQTT_PORT = 1884
LIVING_LAB_USER = "twinlight"
LIVING_LAB_PW = "twinlight"
# Das Topic zum Abonnieren aller Sensor-Updates
# Entnommen aus README.md
MQTT_TOPIC = "middleware/#"

# Diese Funktion wird aufgerufen, wenn die Verbindung zum Broker hergestellt wurde.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Erfolgreich mit dem Living Lab MQTT Broker verbunden.")
        # Abonniere das Topic, um alle Sensor-Updates zu erhalten
        client.subscribe(MQTT_TOPIC)
        print(f"Abonniert auf Topic: '{MQTT_TOPIC}'")
    else:
        print(f"Verbindung fehlgeschlagen mit Code: {rc}")

# Diese Funktion wird jedes Mal aufgerufen, wenn eine Nachricht auf einem abonnierten Topic empfangen wird.
def on_message(client, userdata, msg):
    # Das Topic ist im Format "middleware/<DEVICE>/<PARAM>"
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 3:
        device = topic_parts[1]
        param = topic_parts[2]
        value = msg.payload.decode('utf-8')
        print(f"Sensor-Update: [Gerät: {device}] [Parameter: {param}] = {value}")

# Hauptteil des Skripts
if __name__ == "__main__":
    # Erstelle einen neuen MQTT-Client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Setze den Benutzernamen und das Passwort für die Authentifizierung
    client.username_pw_set(LIVING_LAB_USER, LIVING_LAB_PW)

    # Weise die Callback-Funktionen zu
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Verbinde mit Living Lab Broker unter {LIVING_LAB_IP}:{LIVING_LAB_MQTT_PORT}...")

    try:
        # Stelle die Verbindung her
        client.connect(LIVING_LAB_IP, LIVING_LAB_MQTT_PORT, 60)

        # Starte eine Endlosschleife, um auf Nachrichten zu lauschen.
        # Das Skript läuft, bis du es manuell stoppst (z.B. mit Strg+C).
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nProgramm wird beendet.")
        client.disconnect()
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
