beforeAll {

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
    sensors [ "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "0", "0", "0", "0" ]
    followUpAction [ "1", "1", "1", "1"]
}



afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
