beforeAll {

    // precondition "sun.sun" feature "state" equals "above_horizon" skipMessage "This scenario must be tested at daylight"

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.arbeitsplatz_helligkeit" feature "state"
        valOff "0"
        valOn "1"
        minChangePercent 0.01
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "1"
        minChangePercent 0.01
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

}

beforeEach {
    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "TC_S5_Proportionality_100" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}

test "TC_S5_Proportionality_80" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "20" ]
    followUpAction [ "80" ]
}

test "TC_S5_Proportionality_60" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "40" ]
    followUpAction [ "60" ]
}


afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
