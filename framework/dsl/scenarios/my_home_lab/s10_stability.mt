beforeAll {

   // precondition "sun.sun" feature "state" equals "below_horizon" skipMessage "This scenario must be tested at night"

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

test "TC_S10_Stability_esp_c6" {
    relation: stability tolerance: 0.05 duration: 80.0
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state" ]
    
    // The lamp is set to 2% and the sensor value is checked for stability for 200 seconds.
    sourceAction [ "2" ]
}



afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
