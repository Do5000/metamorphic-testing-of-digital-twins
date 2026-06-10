beforeAll {

// Calibrations for switch.licht_schalter

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
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

calibrate_latency {
    actuator "switch.licht_schalter" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "switch.licht_schalter" feature "state" to "0"

// Calibrations for WP1 (light.norden_fenster)

calibrate_latency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"

// Calibrations for WP2 (light.sueden_fenster)

calibrate_latency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"

calibrate_latency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"

// Calibrations for Illuminance.Room518a_Ceiling

calibrate_latency {
    actuator "light.norden_tuer" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.norden_tuer" feature "state" to "0"

calibrate_latency {
    actuator "light.sueden_tuer" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    val_off "0"
    val_on "1"
    min_change_percent 0.05
    tolerance_factor 1.1
    add_seconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_tuer" feature "state" to "0"


}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
}

// Tests with switch.licht_schalter

test "test_monotonicity_Illuminance_Room518a_Ceiling_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_Illuminance_Room518a_Ceiling_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL1_LowerScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL1_LowerScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL1_LowerScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL1_LowerScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL2_Keyboard_spec_Room518a_WP1_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL2_Keyboard_spec_Room518a_WP1_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL2_Keyboard_spec_Room518a_WP2_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL2_Keyboard_spec_Room518a_WP2_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL3_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL3_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL3_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL3_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL4_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL4_UpperScreen_spec_Room518a_WP1_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL4_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL4_UpperScreen_spec_Room518a_WP2_switch_licht_schalter" {
    relation: not monotonicity
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


// Tests for WP1

test "test_monotonicity_TSL1_LowerScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL1_LowerScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: not monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster" {
    relation: monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster" {
    relation: not monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL3_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL3_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: not monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL4_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL4_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: not monotonicity
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


// Tests for WP2

test "test_monotonicity_TSL1_LowerScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL1_LowerScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: not monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL2_Keyboard_spec_Room518a_WP2_light_sueden_fenster" {
    relation: monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL2_Keyboard_spec_Room518a_WP2_light_sueden_fenster" {
    relation: not monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL3_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL3_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: not monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_TSL4_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_TSL4_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: not monotonicity
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


// Tests with sensor Illuminance.Room518a_Ceiling

test "test_monotonicity_Illuminance_Room518a_Ceiling_light_norden_tuer" {
    relation: monotonicity
    actuators [ "light.norden_tuer" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_Illuminance_Room518a_Ceiling_light_norden_tuer" {
    relation: not monotonicity
    actuators [ "light.norden_tuer" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}


test "test_monotonicity_Illuminance_Room518a_Ceiling_light_sueden_tuer" {
    relation: monotonicity
    actuators [ "light.sueden_tuer" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "0" ]
    followup_action [ "1" ]
}

test "test_inverse_monotonicity_Illuminance_Room518a_Ceiling_light_sueden_tuer" {
    relation: not monotonicity
    actuators [ "light.sueden_tuer" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    source_action [ "1" ]
    followup_action [ "0" ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}
