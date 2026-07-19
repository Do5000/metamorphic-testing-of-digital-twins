beforeAll {

set "switch.licht_schalter" feature "state" to "0"

calibrateLatency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

calibrateLatency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

}

beforeEach {
    set "light.norden_fenster" feature "state" to "0"
}

test "test_substitution_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_0" {
    relation: substitution tolerance: 0.05 profile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ 0 ]
}

test "test_substitution_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_30" {
    relation: substitution tolerance: 0.05 profile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ 30 ]
}

test "test_substitution_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_60" {
    relation: substitution tolerance: 0.05 profile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ 60 ]
}

test "test_substitution_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_100" {
    relation: substitution tolerance: 0.05 profile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ 100 ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}