beforeAll {

set "switch.licht_schalter" feature "state" to "0"

// Calibrations for sensor Illuminance.Room518a_Ceiling

calibrateLatency {
    actuator "switch.licht_schalter" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"


}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_norden_tuer_light_sueden_tuer" {
    relation: conservation tolerance: 0.10
    actuators [ "light.norden_tuer" feature "state", "light.sueden_tuer" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_norden_tuer_light__norden_fenster" {
    relation: conservation tolerance: 0.10
    actuators [ "light.norden_tuer" feature "state", "light.norden_fenster" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_norden_tuer_light__sueden_fenster" {
    relation: conservation tolerance: 0.10
    actuators [ "light.norden_tuer" feature "state", "light.sueden_fenster" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_sueden_tuer_light__sueden_fenster" {
    relation: conservation tolerance: 0.10
    actuators [ "light.sueden_tuer" feature "state", "light.sueden_fenster" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_sueden_tuer_light__norden_fenster" {
    relation: conservation tolerance: 0.10
    actuators [ "light.sueden_tuer" feature "state", "light.norden_fenster" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_Illuminance_Room518a_Ceiling_light_norden_fenster_light_sueden_fenster" {
    relation: conservation tolerance: 0.10
    actuators [ "light.norden_fenster" feature "state", "light.sueden_fenster" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}


// Inverse Tests that should show that light from other Workplaces contributes less to a other workplace than the light directly above workplace
test "test_conservation_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_light_sueden_fenster" {
    relation: not conservation tolerance: 0.10
    actuators [ "light.norden_fenster" feature "state", "light.sueden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "test_conservation_TSL2_Keyboard_spec_Room518a_WP2_light_norden_fenster_light_sueden_fenster" {
    relation: not conservation tolerance: 0.10
    actuators [ "light.norden_fenster" feature "state", "light.sueden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}