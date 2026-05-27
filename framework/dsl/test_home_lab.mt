beforeAll {
    precondition "automation.nach_sonnenuntergang" feature "state" equals "on" skip_message "Tests require the sun to be below the horizon."
    
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    
    calibrate_latency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        val_off "off"
        val_on "on"
        min_change_percent 0.2
        tolerance_factor 1.1
        add_seconds 0
        timeout 3.0
        runs 1
    }
    
    set "light.schreibtisch_lampe" feature "state" to "off"
    
    calibrate_latency {
        actuator "light.amelie_lampe" feature "state"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        val_off "off"
        val_on "on"
        min_change_percent 0.1
        tolerance_factor 1.1
        add_seconds 1
        timeout 3.0
        runs 1
    }
}

beforeEach {
    set "switch.fernseher_ecke_steckdose" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.amelie_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "test_home_monotony" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    source_action [ "0" ]
    followup_action [ "2" ]
}

test "test_home_invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    source_action [ "on" ]
    followup_action [ "on" ]
}

test "test_home_conservation" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "state", "light.amelie_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    source_action [ "on", "off" ]
    followup_action [ "off", "on" ]
}

test "test_sensor_stability" {
    relation: stability tolerance: 0.05 duration: 15.0
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    source_action [ "on" ]
}

test "test_light_proportionality" {
    relation: proportionality tolerance: 0.2
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    source_action [ "off" ]
    followup_action [ "on" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "switch.fernseher_ecke_steckdose" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.amelie_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
