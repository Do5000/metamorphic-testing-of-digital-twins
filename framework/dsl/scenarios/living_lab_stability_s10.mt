beforeAll {

// Calibration for switch.licht_schalter

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}

}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
}



test "test_stability_Illuminance_Room518a_Ceiling_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "1" ]
}

test "test_stability_TSL1_LowerScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL1_LowerScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL2_Keyboard_spec_Room518a_WP1_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL2_Keyboard_spec_Room518a_WP2_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL3_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL3_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL4_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
}

test "test_stability_TSL4_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: stability tolerance: 0.05 duration: 20.0
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}