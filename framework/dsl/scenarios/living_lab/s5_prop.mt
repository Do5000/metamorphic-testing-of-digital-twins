beforeAll {

    // precondition "sun.sun" feature "state" equals "below_horizon" skipMessage "This scenario must be tested at daylight"


    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"


    calibrateLatency {
        actuator "light.norden_tuer" feature "brightness"
        sensor "Illuminance.Room518a_Ceiling" feature "Illuminance"
        valOff "0"
        valOn "1"
        minChangePercent 0.03
        maxSettleTolerance 0.03
        settleTime 20.0
        toleranceFactor 1
        addSeconds 10
        timeout 90.0
        runs 1
    }

}

beforeEach {
    set "light.norden_tuer" feature "brightness" to "0"
    set "light.norden_fenster" feature "brightness" to "0"
    set "light.sueden_tuer" feature "brightness" to "0"
    set "light.sueden_fenster" feature "brightness" to "0"
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
