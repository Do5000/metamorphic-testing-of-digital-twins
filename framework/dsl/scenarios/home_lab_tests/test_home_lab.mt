beforeAll {
    precondition "sun.sun" feature "state" equals "above_horizon" skipMessage "Tests require the sun to be below the horizon."
    
    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    
    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "off"
        valOn "on"
        minChangePercent 0.01
        toleranceFactor 1.5
        addSeconds 2
        timeout 3.0
        runs 1
    }
    
    set "light.schreibtisch_lampe" feature "state" to "off"
    
    calibrateLatency {
        actuator "light.amelie_lampe" feature "brightness"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.01
        toleranceFactor 1.5
        addSeconds 2
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
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}

test "test_home_monotony_inverted" {
    relation: not monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "100" ]
    followUpAction [ "0" ]
}


test "test_home_invariance" {
    relation: invariance tolerance: 0.01
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "on" ]
    intermediateAction ["off"]
    followUpAction [ "on" ]
}

test "test_home_conservation" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "state", "light.amelie_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "on", "off" ]
    followUpAction [ "off", "on" ]
}

test "test_light_proportionality_inverted_s5" {
    relation: not proportionality tolerance: 0.01
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "off" ]
    followUpAction [ "on" ]
}

test "test_sensor_stability" {
    relation: stability tolerance: 0.05 duration: 15.0
    actuators [ "light.schreibtisch_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "on" ]
}



afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "switch.fernseher_ecke_steckdose" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.amelie_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
