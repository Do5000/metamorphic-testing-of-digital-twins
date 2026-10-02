
beforeAll {

    // precondition "sun.sun" feature "state" equals "below_horizon" skipMessage "Tests require the sun to be below the horizon."

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
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.vintage_lampe" feature "state"
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

test "TC_S8_Monotony" {
    relation: monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}

test "TC_S8_Monotony_Inverted" {
    relation: not monotonicity
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "100" ]
    followUpAction [ "0" ]
}

test "TC_S8_Invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    sourceAction [ "100" ]
    intermediateAction [ "0" ]
    followUpAction [ "100" ]
}

test "TC_S8_Conservation_100" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "100", "0" ]
    followUpAction [ "0", "100" ]
}

test "TC_S8_Conservation_90" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "90", "10" ]
    followUpAction [ "10", "90" ]
}

test "TC_S8_Conservation_75" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "75", "25" ]
    followUpAction [ "25", "75" ]
}

test "TC_S8_Conservation_65" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "65", "35" ]
    followUpAction [ "35", "65" ]
}


afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
