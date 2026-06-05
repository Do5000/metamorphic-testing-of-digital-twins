beforeAll {
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "test_invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    source_action [ "on" ]
    intermediate_action ["off"]
    followup_action [ "on" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
