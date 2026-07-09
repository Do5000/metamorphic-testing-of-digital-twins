beforeAll {
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "generate_sensor_profile" {
    relation: generation historicalFile: "sensor_profile.json"
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    brightnessLevels = [0,10,20,30,40,50,60,70,80,90,100]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
