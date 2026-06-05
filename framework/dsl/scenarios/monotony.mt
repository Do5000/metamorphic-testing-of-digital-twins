beforeAll {
    precondition "automation.nach_sonnenuntergang" feature "state" equals "0" skip_message "Tests require the sun to be below the horizon."

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrate_latency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        val_off "off"
        val_on "on"
        min_change_percent 0.01
        tolerance_factor 1.4
        add_seconds 0
        timeout 5.0
        runs 3
    }

}

test "test_monotonicity" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    source_action [ "off" ]
    followup_action [ "on" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
