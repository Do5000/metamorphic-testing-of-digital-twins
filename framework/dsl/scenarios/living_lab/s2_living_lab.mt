beforeAll {



}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}


test "TC_S2_Invariance_Ceiling" {
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

test "TC_S2_Invariance_Keyboard_WP1" {
    relation: invariance tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "0.75", "0.75", "0.75", "0.75" ]
    intermediateAction [ "0", "0", "0", "0" ]
    followUpAction [ "0.75", "0.75", "0.75", "0.75" ]
}

test "TC_S2_Invariance_Keyboard_WP2" {
    relation: invariance tolerance: 0.02
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec" ]
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
