beforeAll {
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "test_sensor_substitution" {
    relation: substitution tolerance: 0.1 profile: "sensor_profile.json"
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    source_action [ 60 ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
