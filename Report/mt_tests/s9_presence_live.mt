beforeAll {
    // S9: The presence sensor must be 0 (Live testing / Context).
    precondition "binary_sensor.arbeitsplatz_praesenz" feature "state" equals "0" skipMessage "Test requires that nobody is in the room."
    
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "1"
        minChangePercent 0.01
        toleranceFactor 1.2
        addSeconds 2
        timeout 3.0
        runs 1
    }
}

beforeEach {
    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "TC_S9_No_Presence_Monotony" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
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
