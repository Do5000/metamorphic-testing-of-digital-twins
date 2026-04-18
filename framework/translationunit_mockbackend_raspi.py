import requests
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event
import logging

from ut_ditto_mock import DittoWebSocket
from ut_mqtt_endpoints import EndpointMQTTandHTTP, parse

# ============================================================================== #
#                       EIGENE KONFIGURATION (RASPBERRY PI)                      #
# ============================================================================== #
RASPI_IP = "192.168.8.30"         # <- HIER DEINE RASBERRY PI IP EINTRAGEN
RASPI_MQTT_PORT = 1883             # <- Standard MQTT Port auf dem Raspi
RASPI_HTTP_PORT = 8123             # <- Standard HomeAssistant Port
RASPI_MQTT_USER = None
RASPI_MQTT_PW = None
RASPI_HA_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiODE3YmNmODAzOTA0NmJlODk3Y2E3ZjZlYzliZTdiYyIsImlhdCI6MTc3NjUwNTI5OCwiZXhwIjoyMDkxODY1Mjk4fQ.3-cMkSJwvPKFtOIl2hz423qcLbO2L3bOq0esSmB-Owk"   # <- HIER DEINEN LONG-LIVED ACCESS TOKEN EINTRAGEN
# ============================================================================== #

class RaspiHomeAssistant(EndpointMQTTandHTTP):
    """
    Diese Klasse fungiert exakt wie deine bisherige `Middleware`- oder `Homeassistant`-Klasse,
    leitet aber alle Befehle und Updates direkt an deinen laufenden Home Assistant Webserver
    und MQTT Broker auf dem Raspberry Pi weiter.
    """
    def __init__(self):
        super().__init__(RASPI_IP, RASPI_MQTT_PORT, RASPI_MQTT_USER, RASPI_MQTT_PW, ["homeassistant/#"])

    def parse_mqtt_message(self, message):
        """ Parst eingehende MQTT Sensordaten von Home Assistant """
        parts = message.topic.split('/')
        # Falls das Topic z.b. homeassistant/sensor/illuminance ist
        if len(parts) >= 4:
            device = f'{parts[1]}.{parts[2]}'
            param = parts[3]
            return (device, param, message.payload.decode())
        return ("", "", "")

    def parse_from_hono(self, vals):
        """ Konvertiert Werte aus Hono in das Home Assistant Format """
        if 'state' in vals:
            vals['state'] = 'on' if parse(int, vals['state'], 0) == 1 else 'off'
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) * 255
        return vals

    def parse_to_hono(self, vals):
        """ Konvertiert Werte von Home Assistant zurück in das Hono / Digital Twin Format """
        if 'state' in vals:
            val = vals['state']
            # Home Assistant "on"/"off"-Schalter in 1/0 umwandeln
            if str(val).lower() == 'on':
                vals['state'] = 1
            elif str(val).lower() == 'off':
                vals['state'] = 0
            else:
                # Echte Sensorwerte (wie 450 Lux vom Arduino) als Zahl durchreichen!
                try:
                    vals['state'] = float(val)
                except ValueError:
                    vals['state'] = val
                    
        if 'brightness' in vals:
            vals['brightness'] = parse(float, vals['brightness'], 0) / 255.0
        return vals

    def send_value(self, device, param_values):
        """ Sendet eine Zustandsänderung (z.B. Lampe ein/aus) an Home Assistant """
        param_values = self.parse_from_hono(param_values)
        
        domain = device.split('.')[0]  # extrahiert "switch" aus "switch.vintage_steckdose"
        
        # Um physische Geräte wie IKEA-Schalter wirklich zu schalten, rufen wir 
        # die Services API auf, nicht die interne States API!
        state = param_values.get('state', 'on')
        service = "turn_on" if state == "on" else "turn_off"
        
        payload = {"entity_id": device}
        
        # Zusatzparameter für Lampen hinzufügen (z.B. Helligkeit)
        if domain == "light" and service == "turn_on" and "brightness" in param_values:
            payload["brightness"] = int(param_values["brightness"])
            
        requests.post(
            f'http://{RASPI_IP}:{RASPI_HTTP_PORT}/api/services/{domain}/{service}',
            headers={
                'Authorization': RASPI_HA_TOKEN,
                'Content-Type': 'application/json'
            },
            json=payload
        )


# ============================================================================== #
#            FRAMEWORK BINDING (Exakt wie translationunit_mockbackend)           #
# ============================================================================== #
logging.getLogger("werkzeug").setLevel(logging.ERROR)

executor = ThreadPoolExecutor(max_workers=10)
raspi_ha = RaspiHomeAssistant()
ditto_mock = DittoWebSocket("0.0.0.0", 8082)

def ditto_mock_on_message(device, param, value):
    # Eingehender Befehl vom Framework -> Leite weiter an Raspberry Pi (HomeAssistant)
    if value is not None and param != "errors-response":
        executor.submit(raspi_ha.send_value, device, {param: value})
    else:
        print(f"Info (Hono:{device}):", param, value)

def raspi_ha_on_device_param_updated(device, param, value):
    # Physischer Sensor-Update vom Raspberry Pi -> Leite weiter an den Mock (Ditto)
    if not device: return
    param_val = raspi_ha.parse_to_hono({param: value})
    param, value_converted = list(param_val.items())[0]
    
    if value_converted is not None:
        ditto_mock.set_feature(device, param, value_converted)
    else:
        print("Info:", param_val)

def run_ditto_mock_http_endpoint(app):
    app.run(host="0.0.0.0", port=8083, debug=False)

def main():
    ditto_mock.on_command = ditto_mock_on_message
    raspi_ha.on_device_param_updated = raspi_ha_on_device_param_updated
    
    app = ditto_mock.create_flask_app()
    Thread(target=run_ditto_mock_http_endpoint, args=(app,), daemon=True).start()
    
    print(f"[*] Verbinde mit Raspberry Pi MQTT Broker unter {RASPI_IP}:{RASPI_MQTT_PORT}...")
    raspi_ha.connect_mqtt()
    ditto_mock.thread.start()
    
    stop = Event()
    try:
        print("[*] Eigene Living Lab Backend-Simulation läuft! (Beenden mit STRG+C)")
        stop.wait()
    except KeyboardInterrupt:
        print("\n[*] Beende Simulation...")
    finally:
        executor.shutdown(wait=True)
        ditto_mock.disconnect()
        raspi_ha.disconnect_mqtt()

if __name__ == "__main__":
    main()
