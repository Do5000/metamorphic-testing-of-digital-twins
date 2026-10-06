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

test "TC_S1_Monotony_100" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}


test "TC_S1_Monotony_80" {
    relation: monotonicity tolerance: 0.02
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "20" ]
    followUpAction [ "80" ]
}


afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
