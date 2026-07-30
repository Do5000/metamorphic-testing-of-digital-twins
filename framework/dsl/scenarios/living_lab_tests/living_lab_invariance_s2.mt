beforeAll {

set "switch.licht_schalter" feature "state" to "0"

// Calibrations for switch.licht_schalter

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


// Calibrations for WP1 (light.norden_fenster)

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
    set "light.norden_fenster" feature "brightness" to 0.0

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
    set "light.norden_fenster" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"
    set "light.norden_fenster" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.norden_fenster" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.norden_fenster" feature "state" to "0"
    set "light.norden_fenster" feature "brightness" to 0.0


// Calibrations for WP2 (light.sueden_fenster)

calibrateLatency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"
    set "light.sueden_fenster" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"
    set "light.sueden_fenster" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"
    set "light.sueden_fenster" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.sueden_fenster" feature "state"
    sensor "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_fenster" feature "state" to "0"
    set "light.sueden_fenster" feature "brightness" to 0.0


// Calibrations with sensor Illuminance.Room518a_Ceiling

calibrateLatency {
    actuator "light.norden_tuer" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.norden_tuer" feature "state" to "0"
    set "light.norden_tuer" feature "brightness" to 0.0

calibrateLatency {
    actuator "light.sueden_tuer" feature "state"
    sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
    valOff "0"
    valOn "1"
    minChangePercent 0.05
    toleranceFactor 1.1
    addSeconds 5
    timeout 40.0
    runs 1
}
set "light.sueden_tuer" feature "state" to "0"
    set "light.sueden_tuer" feature "brightness" to 0.0

}

beforeEach {
    set "switch.licht_schalter" feature "state" to "0"
}

// Invariance Tests with switch.licht_schalter

test "test_invariance_Illuminance_Room518a_Ceiling_switch_licht_schalter" {
    relation: invariance tolerance: 0.05
    actuators [ "switch.licht_schalter" feature "state" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1" ]
    intermediateAction ["0"]
    followUpAction [ "1" ]
}

// Invariance Tests for WP1 (light.norden_fenster)

test "test_invariance_TSL1_LowerScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_fenster" feature "state", "light.norden_fenster" feature "brightness" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL2_Keyboard_spec_Room518a_WP1_light_norden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_fenster" feature "state", "light.norden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL3_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_fenster" feature "state", "light.norden_fenster" feature "brightness" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL4_UpperScreen_spec_Room518a_WP1_light_norden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_fenster" feature "state", "light.norden_fenster" feature "brightness" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}


// Invariance Tests for WP2 (light.sueden_fenster)

test "test_invariance_TSL1_LowerScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "state", "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL1_LowerScreen_spec.Room518a_WP2" feature "TSL1_LowerScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL2_Keyboard_spec_Room518a_WP2_light_sueden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "state", "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL3_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "state", "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL3_UpperScreen_spec.Room518a_WP2" feature "TSL3_UpperScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_TSL4_UpperScreen_spec_Room518a_WP2_light_sueden_fenster" {
    relation: invariance tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "state", "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL4_UpperScreen_spec.Room518a_WP2" feature "TSL4_UpperScreen_spec" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}


// Invariance Tests with sensor Illuminance.Room518a_Ceiling

test "test_invariance_Illuminance_Room518a_Ceiling_light_norden_tuer" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_tuer" feature "state", "light.norden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

test "test_invariance_Illuminance_Room518a_Ceiling_light_sueden_tuer" {
    relation: invariance tolerance: 0.05
    actuators [ "light.sueden_tuer" feature "state", "light.sueden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", 1.0 ]
    intermediateAction [ "0", 0.0 ]
    followUpAction [ "1", 1.0 ]
}

afterAll {
    set "switch.licht_schalter" feature "state" to "0"
}