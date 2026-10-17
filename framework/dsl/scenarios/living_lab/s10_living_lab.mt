beforeAll {



}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0.17"
    set "light.norden_fenster" feature "brightness" to "0.17"
    set "light.sueden_tuer" feature "brightness" to "0.17"
    set "light.sueden_fenster" feature "brightness" to "0.17"
}

test "TC_S10_Stability" {
    relation: stability tolerance: 0.05 duration: 300.0
    actuators [ "light.norden_tuer" feature "brightness",
        "light.sueden_tuer" feature "brightness",
        "light.sueden_fenster" feature "brightness",
        "light.norden_fenster" feature "brightness"  ]
    sensors [ "Illuminance.Room518a_Ceiling" feature "Illuminance" ]
    sourceAction [ "0.17", "0.17", "0.17", "0.17" ]

}



afterAll {
    set "light.norden_tuer" feature "brightness" to "0.17"
    set "light.norden_fenster" feature "brightness" to "0.17"
    set "light.sueden_tuer" feature "brightness" to "0.17"
    set "light.sueden_fenster" feature "brightness" to "0.17"
}
