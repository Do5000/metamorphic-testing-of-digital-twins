beforeAll {
    precondition "automation.nach_sonnenuntergang" feature "state" equals "0" skipMessage "Tests require the sun to be below the horizon."

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "off"
        valOn "on"
        minChangePercent 0.01
        toleranceFactor 1.4
        addSeconds 0
        timeout 5.0
        runs 3
    }

}

test "test_monotonicity" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "off" ]
    followUpAction [ "on" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
