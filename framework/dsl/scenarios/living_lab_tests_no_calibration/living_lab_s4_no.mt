beforeAll {

set "switch.licht_schalter" feature "state" to "0"
set "light.neues_licht" feature "state" to "0"
set "light.neues_licht" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.neues_licht" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}

}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
    set "light.neues_licht" feature "state" to "0"
    set "light.neues_licht" feature "brightness" to 0.0
}

test "test_monotonicity_Illuminance_Room518a_Ceiling_light_neues_licht" {
    relation: monotonicity
    actuators [ "light.neues_licht" feature "state", "light.neues_licht" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_inverse_monotonicity_Illuminance_Room518a_Ceiling_light_neues_licht" {
    relation: not monotonicity
    actuators [ "light.neues_licht" feature "state", "light.neues_licht" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", 1.0 ]
    followUpAction [ "0", 0.0 ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
    set "light.neues_licht" feature "state" to "0"
    set "light.neues_licht" feature "brightness" to 0.0
}