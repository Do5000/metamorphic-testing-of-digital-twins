import requests
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event
import logging

from ut_ditto_mock import DittoWebSocket
from ut_mqtt_endpoints import EndpointMQTTandHTTP, parse
import websockets
import asyncio

# ============================================================================== #
#                       EIGENE KONFIGURATION (RASPBERRY PI)                      #
# ============================================================================== #
RASPI_IP = "192.168.8.30"         # <- HIER DEINE RASBERRY PI IP EINTRAGEN
RASPI_MQTT_PORT = 1883             # <- Standard MQTT Port auf dem Raspi
RASPI_HTTP_PORT = 8123             # <- Standard HomeAssistant Port
RASPI_MQTT_USER = "mqtt_user"
RASPI_MQTT_PW = "mqtt_password"
RASPI_HA_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2NzA4YmQ4MjViMzg0YWM1ODQ1NWExNWMyYWM1MmE3OSIsImlhdCI6MTc3NzE0MTI3NSwiZXhwIjoyMDkyNTAxMjc1fQ.lHLlrdOIT1CGg-1pv8c-I6Z88Xdv9_jwHEwjKdsPLdI"
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
            val = vals['state']
            if str(val).lower() in ['on', '1', 'true']:
                vals['state'] = 'on'
            else:
                vals['state'] = 'off'
        if 'brightness' in vals:
            b_val = parse(float, vals['brightness'], 0)
            if b_val > 1.0:
                b_val = b_val / 100.0  # Von Prozent in 0..1 umrechnen
            vals['brightness'] = max(0.0, min(1.0, b_val)) * 255

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
            
        print(f"[*] Sende an HA: {domain}/{service} für {device}...")
        
        response = requests.post(
            f'http://{RASPI_IP}:{RASPI_HTTP_PORT}/api/services/{domain}/{service}',
            headers={
                'Authorization': RASPI_HA_TOKEN,
                'Content-Type': 'application/json'
            },
            json=payload
        )
        
        if response.status_code == 200:
            print(f"[+] Erfolgreich geschaltet: {device} | Antwort: {response.text}")
        else:
            print(f"[!] FEHLER beim Schalten: {response.status_code} - {response.text}")

    def sync_from_ha(self, ditto_mock):
        """ Holt alle aktuellen Zustände von HA und registriert sie im Ditto-Mock """
        print(f"[*] Synchronisiere alle Entitäten von Home Assistant ({RASPI_IP})...")
        try:
            response = requests.get(
                f'http://{RASPI_IP}:{RASPI_HTTP_PORT}/api/states',
                headers={
                    'Authorization': RASPI_HA_TOKEN,
                    'Content-Type': 'application/json'
                },
                timeout=10
            )
            if response.status_code == 200:
                entities = response.json()
                for e in entities:
                    e_id = e['entity_id']
                    # Wir überspringen interne HA-Entitäten, die meist nicht relevant sind
                    if e_id.startswith(('person.', 'zone.')):
                        continue
                        
                    state = e['state']
                    # Konvertiere HA-Zustand (on/off) in Hono-Format (1/0)
                    vals = self.parse_to_hono({'state': state})
                    
                    # Zusatz-Attribute (Brightness, Position etc.)
                    attrs = e.get('attributes', {})
                    if 'brightness' in attrs:
                        vals.update(self.parse_to_hono({'brightness': attrs['brightness']}))
                    if 'current_position' in attrs:
                        vals['position'] = attrs['current_position']
                    
                    # Im Mock registrieren
                    for param, val in vals.items():
                        ditto_mock.set_feature(e_id, param, val)
                
                print(f"[+] {len(entities)} Entitäten im Digitalen Zwilling initialisiert.")
            else:
                print(f"[!] Fehler beim Sync: Status {response.status_code}")
        except Exception as e:
            print(f"[!] Sync-Fehler: {e}")

class HAWebSocketListener:
    """
    Hört direkt auf den Home Assistant Websocket, um Echtzeit-Updates zu erhalten.
    Dies ist robuster als MQTT Statestream, da es keine extra Konfiguration in HA benötigt.
    """
    def __init__(self, ip, token, ditto_mock, raspi_ha):
        self.ip = ip
        # HA erwartet im Websocket nur den Token-String ohne "Bearer "
        self.token = token.replace("Bearer ", "").strip()
        self.ditto_mock = ditto_mock
        self.raspi_ha = raspi_ha
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self._run_loop, daemon=True)

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen())

    async def _listen(self):
        url = f"ws://{self.ip}:8123/api/websocket"
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # 1. Authentifizierung
                    await ws.send(json.dumps({"type": "auth", "access_token": self.token}))
                    
                    # 2. Subscription auf alle Zustandsänderungen
                    await ws.send(json.dumps({
                        "id": 1,
                        "type": "subscribe_events",
                        "event_type": "state_changed"
                    }))
                    
                    print(f"[*] HA Websocket: Verbunden und abonniert ({self.ip})")
                    
                    async for msg in ws:
                        data = json.loads(msg)
                        if data.get("type") == "event":
                            event_data = data.get("event", {}).get("data", {})
                            entity_id = event_data.get("entity_id")
                            new_state = event_data.get("new_state")
                            
                            if entity_id and new_state:
                                # Wir ignorieren wieder interne HA-Entitäten
                                if entity_id.startswith(('person.', 'zone.')):
                                    continue
                                    
                                state = new_state.get("state")
                                attrs = new_state.get("attributes", {})
                                
                                # In das Hono/Ditto Format konvertieren
                                vals = self.raspi_ha.parse_to_hono({"state": state})
                                if "brightness" in attrs:
                                    vals.update(self.raspi_ha.parse_to_hono({"brightness": attrs["brightness"]}))
                                if "current_position" in attrs:
                                    vals["position"] = attrs["current_position"]
                                
                                # Im Mock aktualisieren
                                for param, val in vals.items():
                                    self.ditto_mock.set_feature(entity_id, param, val)
            except Exception as e:
                print(f"[!] HA Websocket Fehler: {e}. Reconnect in 5s...")
                await asyncio.sleep(5)

    def start(self):
        self.thread.start()


# ============================================================================== #
#            FRAMEWORK BINDING (Exakt wie translationunit_mockbackend)           #
# ============================================================================== #
logging.getLogger("werkzeug").setLevel(logging.ERROR)

executor = ThreadPoolExecutor(max_workers=1)
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
    # Enable threaded mode to prevent HTTP polls from blocking other logic
    app.run(host="0.0.0.0", port=8083, debug=False, threaded=True)

def main():
    ditto_mock.on_command = ditto_mock_on_message
    raspi_ha.on_device_param_updated = raspi_ha_on_device_param_updated
    
    app = ditto_mock.create_flask_app()
    Thread(target=run_ditto_mock_http_endpoint, args=(app,), daemon=True).start()
    
    # Synchronisiere alle Entitäten von HA VOR dem Start der Listener
    raspi_ha.sync_from_ha(ditto_mock)
    
    # Starte den Websocket Listener für Echtzeit-Updates von HA
    ha_ws = HAWebSocketListener(RASPI_IP, RASPI_HA_TOKEN, ditto_mock, raspi_ha)
    ha_ws.start()
    
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
