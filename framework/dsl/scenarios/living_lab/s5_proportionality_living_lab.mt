beforeAll {



}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}

test "TC_S5_Proportionality_100" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    sourceAction [ "0", "0", "0", "0" ]
    followUpAction [ "1", "1", "1", "1" ]
}

test "TC_S5_Proportionality_80" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    sourceAction [ "0.2", "0.2", "0.2", "0.2" ]
    followUpAction [ "0.8", "0.8", "0.8", "0.8" ]
}

test "TC_S5_Proportionality_60" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "TSL2_Keyboard_spec.Room518a_WP1" feature "TSL2_Keyboard_spec", "TSL1_LowerScreen_spec.Room518a_WP1" feature "TSL1_LowerScreen_spec" ]
    sourceAction [ "0.4", "0.4", "0.4", "0.4" ]
    followUpAction [ "0.6", "0.6", "0.6", "0.6" ]
}

afterAll {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
}
