beforeAll {
    // S9: The presence sensor must be 0 (Live testing / Context).
    precondition "binary_sensor.arbeitsplatz_praesenz" feature "state" equals "0" skipMessage "Test requires that nobody is in the room."

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

beforeEach {
    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "TC_S9_Presence_Monotony" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "binary_sensor.arbeitsplatz_praesenz" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
