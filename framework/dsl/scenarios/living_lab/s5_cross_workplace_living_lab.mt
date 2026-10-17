beforeAll {



}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}

test "TC_S5_cross_workplace_norden_fenster" {
    relation: not proportionality tolerance: 0.5
    actuators [ "light.norden_tuer" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "0.02" ]
    followUpAction [ "0.98" ]
}

test "TC_S5_cross_workplace_sueden_fenster" {
    relation: not proportionality tolerance: 0.5
    actuators [ "light.sueden_fenster" feature "brightness" ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL2_Keyboard_spec.Room518a_WP2" feature "TSL2_Keyboard_spec" ]
    sourceAction [ "0.02" ]
    followUpAction [ "0.98" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
