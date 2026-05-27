beforeAll {
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "generate_sensor_profile" {
    relation: generation historical_samples: 100 historical_file: "sensor_profile.json"
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    brightness_levels = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
