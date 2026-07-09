beforeAll {
    precondition "automation.nach_sonnenuntergang" feature "state" equals "0" skipMessage "Tests require the sun to be below the horizon."

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.amelie_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "off"
        valOn "on"
        minChangePercent 0.1
        toleranceFactor 1.5
        addSeconds 1
        timeout 5.0
        runs 1
    }

    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.amelie_lampe" feature "brightness"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.1
        toleranceFactor 1.5
        addSeconds 1
        timeout 3.0
        runs 1
    }

}

test "conservation" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "state", "light.amelie_lampe" feature "state" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "on", "off" ]
    followUpAction [ "off", "on" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.amelie_lampe" feature "state" to "off"
    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
