beforeAll {

    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"

    calibrateLatency {
        actuator "light.norden_fenster" feature "brightness"
        sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
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

test "TC_S4_Monotony" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

test "TC_S4_Invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_fenster" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.75" ]
    intermediateAction [ "0" ]
    followUpAction [ "0.75" ]
}

test "TC_S4_Conservation_100" {
    relation: conservation tolerance: 0.05
    actuators [ "light.norden_fenster" feature "brightness", "light.sueden_fenster" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
