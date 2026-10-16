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
        runs 1
    }

    set "light.norden_tuer" feature "brightness" to "0"

    calibrateLatency {
        actuator "light.sueden_tuer" feature "brightness"
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

test "TC_S8_Monotony" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0" ]
    followUpAction [ "1" ]
}

test "TC_S8_Invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.75" ]
    intermediateAction [ "0" ]
    followUpAction [ "0.75" ]
}

test "TC_S8_Conservation_100" {
    relation: conservation tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness", "light.sueden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "1", "0" ]
    followUpAction [ "0", "1" ]
}

test "TC_S8_Conservation_90" {
    relation: conservation tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness", "light.sueden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.9", "0.1" ]
    followUpAction [ "0.1", "0.9" ]
}

test "TC_S8_Conservation_75" {
    relation: conservation tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness", "light.sueden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.75", "0.25" ]
    followUpAction [ "0.25", "0.75" ]
}

test "TC_S8_Conservation_65" {
    relation: conservation tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness", "light.sueden_tuer" feature "brightness" ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.65", "0.35" ]
    followUpAction [ "0.35", "0.65" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
