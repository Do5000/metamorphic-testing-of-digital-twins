beforeAll {

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"


    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "brightness"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "100"
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
        actuator "light.nanoleaf_lampe" feature "brightness"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.01
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

    set "light.nanoleaf_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.vintage_lampe" feature "brightness"
        sensor "sensor.arbeitsplatz_helligkeit" feature "state"
        valOff "0"
        valOn "100"
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

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "brightness"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "100"
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
        actuator "light.nanoleaf_lampe" feature "brightness"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.01
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

    set "light.nanoleaf_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.vintage_lampe" feature "brightness"
        sensor "sensor.arbeitsplatz_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.01
        maxSettleTolerance 0.1
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 0.5
        timeout 5.0
        runs 1
    }

    set "light.vintage_lampe" feature "state" to "off"

}

test "TC_S7_Stability" {
    relation: stability tolerance: 0.05 duration: 5.0
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]

    // The lamp is set to 50% and the sensor value is checked for stability for 5 seconds.
    sourceAction [ "50" ]
}

afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}