beforeAll {



}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}


test "TC_S2_Invariance" {
    relation: invariance tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.75", "0.75", "0.75", "0.75" ]
    intermediateAction [ "0", "0", "0", "0" ]
    followUpAction [ "0.75", "0.75", "0.75", "0.75" ]
}


afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
