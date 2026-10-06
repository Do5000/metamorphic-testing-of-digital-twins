
beforeAll {

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.nanoleaf_lampe" feature "brightness"
        sensor "sensor.esp_c6_helligkeit" feature "state"
        valOff "0"
        valOn "100"
        minChangePercent 0.01
        maxSettleTolerance 0.01
        settleTime 5.0
        toleranceFactor 1.2
        addSeconds 1
        timeout 30.0
        runs 1
    }


}

beforeEach {
    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"
}

test "TC_S6_Monotony" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}


test "TC_S6_Invariance" {
    relation: invariance tolerance: 0.05
    actuators [ "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "100" ]
    intermediateAction [ "0" ]
    followUpAction [ "100" ]
}

test "TC_S6_Conservation_100" {
    relation: conservation tolerance: 0.05
    actuators [ "light.nanoleaf_lampe" feature "brightness", "light.vintage_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "100", "0" ]
    followUpAction [ "0", "100" ]
}




afterAll {
    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
