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

test "generate_sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster" {
    relation: generation historicalFile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    brightnessLevels = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
}


test "test_substitution_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster_0" {
    relation: substitution tolerance: 0.05 profile: "sensor_profile_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1.json"
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ 0 ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}