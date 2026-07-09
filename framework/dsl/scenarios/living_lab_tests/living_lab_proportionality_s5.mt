beforeAll {

set "switch.licht_schalter" feature "state" to "0"

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

}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
}

// WP1

// Combination 1: TSL1 & TSL2
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP1_TSL2_Keyboard_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 2: TSL1 & TSL3
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP1_TSL3_UpperScreen_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 3: TSL1 & TSL4
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP1_TSL4_UpperScreen_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 4: TSL2 & TSL3
test "test_proportionality_switch_licht_schalter_TSL2_Keyboard_spec_Room518a_WP1_TSL3_UpperScreen_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec",
        "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 5: TSL2 & TSL4
test "test_proportionality_switch_licht_schalter_TSL2_Keyboard_spec_Room518a_WP1_TSL4_UpperScreen_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec",
        "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 6: TSL3 & TSL4
test "test_proportionality_switch_licht_schalter_TSL3_UpperScreen_spec_Room518a_WP1_TSL4_UpperScreen_spec_Room518a_WP1" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}


// WP2

// Combination 1: TSL1 & TSL2
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP2_TSL2_Keyboard_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec",
        "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 2: TSL1 & TSL3
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP2_TSL3_UpperScreen_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec",
        "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 3: TSL1 & TSL4
test "test_proportionality_switch_licht_schalter_TSL1_LowerScreen_spec_Room518a_WP2_TSL4_UpperScreen_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 4: TSL2 & TSL3
test "test_proportionality_switch_licht_schalter_TSL2_Keyboard_spec_Room518a_WP2_TSL3_UpperScreen_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec",
        "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 5: TSL2 & TSL4
test "test_proportionality_switch_licht_schalter_TSL2_Keyboard_spec_Room518a_WP2_TSL4_UpperScreen_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec",
        "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Combination 6: TSL3 & TSL4
test "test_proportionality_switch_licht_schalter_TSL3_UpperScreen_spec_Room518a_WP2_TSL4_UpperScreen_spec_Room518a_WP2" {
    relation: proportionality tolerance: 0.01
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [
        "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// Inverse Tests that should show that light from other Workplaces contributes less to a other workplace than the light directly above workplace

// TSL1: WP1 vs WP2
test "test_not_proportionality_light_norden_fenster_TS1_WP1_vs_WP2" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec",
        "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL2: WP1 vs WP2
test "test_not_proportionality_light_norden_fenster_TS2_WP1_vs_WP2" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec",
        "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL3: WP1 vs WP2
test "test_not_proportionality_light_norden_fenster_TS3_WP1_vs_WP2" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [
        "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec",
        "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL4: WP1 vs WP2 bei WP1-Licht
test "test_not_proportionality_light_norden_fenster_TS4_WP1_vs_WP2" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.norden_fenster" feature "state" ]
    sensors [
        "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}


// TSL1: WP2 vs WP1
test "test_not_proportionality_light_sueden_fenster_TS1_WP2_vs_WP1" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [
        "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec",
        "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL2: WP2 vs WP1
test "test_not_proportionality_light_sueden_fenster_TS2_WP2_vs_WP1" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [
        "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec",
        "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL3: WP2 vs WP1
test "test_not_proportionality_light_sueden_fenster_TS3_WP2_vs_WP1" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [
        "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec",
        "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

// TSL4: WP2 vs WP1
test "test_not_proportionality_light_sueden_fenster_TS4_WP2_vs_WP1" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.sueden_fenster" feature "state" ]
    sensors [
        "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec",
        "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}