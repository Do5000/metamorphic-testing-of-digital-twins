beforeAll {

    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"


    calibrateLatency {
        actuator "light.norden_tuer" feature "brightness"
        sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 3
    }
    set "light.norden_tuer" feature "state" to "off"



    calibrateLatency {
        actuator "light.sueden_fenster" feature "brightness"
        sensor "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 3
    }

    set "light.sueden_fenster" feature "state" to "off"

    calibrateLatency {
        actuator "light.sueden_tuer" feature "brightness"
        sensor "TSL2_Keyboard_spec.Room518a_Ceiling" feature "TSL2_Keyboard_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 3
    }

    set "light.sueden_tuer" feature "state" to "off"

    calibrateLatency {
        actuator "light.sueden_tuer" feature "brightness"
        sensor "TSL3_UpperScreen_spec.Room518a_WP1" feature "TSL3_UpperScreen_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 3
    }

    set "light.sueden_tuer" feature "state" to "off"

    calibrateLatency {
        actuator "light.sueden_fenster" feature "brightness"
        sensor "TSL4_UpperScreen_spec.Room518a_WP1" feature "TSL4_UpperScreen_spec"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 3
    }

}

beforeEach {

    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"


}

test "TC_S7_Stability" {
    relation: stability tolerance: 0.05 duration: 60.0
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]


    sourceAction [ "1" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}