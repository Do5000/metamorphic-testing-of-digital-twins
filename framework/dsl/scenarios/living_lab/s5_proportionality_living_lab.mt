beforeAll {

    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"

    calibrateLatency {
        actuator "light.sueden_fenster" feature "brightness"
        sensor "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 1
    }

    set "light.sueden_fenster" feature "brightness" to "0"

    calibrateLatency {
        actuator "light.sueden_fenster" feature "brightness"
        sensor "TSL1_LowerSreen_spec.Room518a_WP1" feature "TSL1_LowerSreen_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 1
    }

}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}

test "TC_S5_Proportionality_100" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerSreen_spec.Room518a_WP1" feature "TSL1_LowerSreen_spec" ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

test "TC_S5_Proportionality_80" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerSreen_spec.Room518a_WP1" feature "TSL1_LowerSreen_spec" ]
    sourceAction [ "0.2" ]
    followUpAction [ "0.8" ]
}

test "TC_S5_Proportionality_60" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerSreen_spec.Room518a_WP1" feature "TSL1_LowerSreen_spec" ]
    sourceAction [ "0.4" ]
    followUpAction [ "0.6" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
