from ut_ditto_mock import DittoWebSocket
import random

class ReactingDittoWebSocket(DittoWebSocket):
    """
    Simulates the physical behavior of the environment without needing the real middleware.
    When actuators are triggered, their effects on the mock 'sensors' are instantly calculated.
    """
    def __init__(self, host, port):
        super().__init__(host, port)

    def set_feature(self, device, feature, value):
        # Update the requested characteristic normally
        super().set_feature(device, feature, value)
        
        # Trigger physics rules to update dependent sensors
        self._simulate_physics()

    def _get_feat_val(self, device, feature, default=0):
        dev_id = f'at.uibk.ut.tenants:{device}'
        try:
            return float(self.devices[dev_id]['features'][feature]['properties']['value'])
        except (KeyError, TypeError, ValueError):
            return default

    def _simulate_physics(self):
        # 1. Monotonicity Test Rules
        # actuator: switch.licht_schalter (state)
        # sensor: TSL2_Keyboard_spec.Room518a_WP1 (TSL2_Keyboard_spec)
        schalter_state = self._get_feat_val('switch.licht_schalter', 'state', 0)
        tsl2_val = 10.0 + (90.0 if schalter_state == 1 else 0.0)
        
        # Update sensor directly without triggering physics recursively
        super().set_feature('TSL2_Keyboard_spec.Room518a_WP1', 'TSL2_Keyboard_spec', tsl2_val)

        # 2. Invariance & Conservation Test Rules
        # actuators: light.norden_tuer (brightness), light.sueden_tuer (brightness)
        # sensor: Illuminance.Room518a_Ceiling (Illuminance)
        n_bright = self._get_feat_val('light.norden_tuer', 'brightness', 0)
        s_bright = self._get_feat_val('light.sueden_tuer', 'brightness', 0)
        
        # Base room illuminance = 50. Each light adds illuminance directly.
        # Adding some jitter to simulate real noise and test the logic tolerance.
        jitter = random.uniform(-0.1, 0.1)
        illuminance_val = 50.0 + n_bright + s_bright + jitter
        
        # Update Ceiling Illuminance
        super().set_feature('Illuminance.Room518a_Ceiling', 'Illuminance', illuminance_val)
        # 3. Deliberately broken physics rule to trigger a test failure
        # actuator: light.norden_fenster (brightness)
        # sensor: Illuminance.Room518a_Window (Illuminance)
        nf_bright = self._get_feat_val('light.norden_fenster', 'brightness', 0)
        
        # BUG: The more light you turn on, the dunkler it gets! (Negative correlation)
        fake_illuminance = 100.0 - nf_bright 
        
        super().set_feature('Illuminance.Room518a_Window', 'Illuminance', fake_illuminance)
