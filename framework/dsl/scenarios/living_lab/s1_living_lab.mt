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

}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}


test "TC_S1_Monotony_all" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0", "0", "0", "0" ]
    followUpAction [ "1", "1", "1", "1"]
}

test "TC_S1_Monotony_sueden_tuer" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.sueden_tuer" feature "brightness"]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0"]
    followUpAction [ "1"]
}

test "TC_S1_Monotony_sueden_fenster" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.sueden_fenster" feature "brightness"]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0"]
    followUpAction [ "1"]
}

test "TC_S1_Monotony_norden_fenster" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.norden_fenster" feature "brightness"]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0"]
    followUpAction [ "1"]
}

test "TC_S1_Monotony_norden_tuer" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness"]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0"]
    followUpAction [ "1"]
}


afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
