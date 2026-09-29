beforeAll {

    // precondition "sun.sun" feature "state" equals "above_horizon" skipMessage "This scenario must be tested at daylight"

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

    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.nanoleaf_lampe" feature "state"
        sensor "sensor.esp_c3_helligkeit" feature "state"
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

test "TC_S5_cross_workplace_schreibtisch_lampe" {
    relation: not proportionality tolerance: 0.5
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "2" ]
    followUpAction [ "98" ]
}

test "TC_S5_cross_workplace_nanoleaf_lampe" {
    relation: not proportionality tolerance: 0.5
    actuators [ "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "2" ]
    followUpAction [ "98" ]
}



afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"


    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
