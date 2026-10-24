beforeAll {

    // precondition "sun.sun" feature "state" equals "above_horizon" skipMessage "This scenario must be tested at daylight"

    set "automation.wohnzimmer_ein" feature "state" to "off"
    set "automation.wohnzimmer_aus" feature "state" to "off"

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "brightness"
        sensor "sensor.arbeitsplatz_helligkeit" feature "state"
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
        runs 1
    }

    set "light.schreibtisch_lampe" feature "state" to "off"

    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "brightness"
        sensor "sensor.esp_c3_helligkeit" feature "state"
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

test "TC_S5_Proportionality_Synchronous_Scaling_80" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state" ]
    sourceAction [ "20", "20", "20" ]
    followUpAction [ "80", "80", "80" ]
}

test "TC_S5_Proportionality_Synchronous_Scaling_60" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state" ]
    sourceAction [ "40", "40", "40" ]
    followUpAction [ "60", "60", "60" ]
}

test "TC_S5_Proportionality_Synchronous_Scaling_50" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state" ]
    sourceAction [ "10", "10", "10" ]
    followUpAction [ "50", "50", "50" ]
}

test "TC_S5_Proportionality_All_Lamps_Full_Scale" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state" ]
    sourceAction [ "0", "0", "0" ]
    followUpAction [ "100", "100", "100" ]
}

test "TC_S5_Proportionality_Desk_Primary_All_Sensors" {
    relation: proportionality tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.arbeitsplatz_helligkeit" feature "state", "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state" ]
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
