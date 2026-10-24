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

test "TC_S3_Conservation_Balanced_Split" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state", "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "40", "30", "30" ]
    followUpAction [ "30", "40", "30" ]
}

test "TC_S3_Conservation_Cyclic_Shift" {
    relation: conservation tolerance: 0.5
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state", "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "50", "30", "20" ]
    followUpAction [ "20", "50", "30" ]
}

test "TC_S3_Conservation_Asymmetric_Split" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state", "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "60", "20", "20" ]
    followUpAction [ "20", "20", "60" ]
}

test "TC_S3_Conservation_Equal_Redistribution" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state", "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "34", "33", "33" ]
    followUpAction [ "33", "34", "33" ]
}

test "TC_S3_Conservation_Single_Luminaire_Swap" {
    relation: conservation tolerance: 0.05
    actuators [ "light.schreibtisch_lampe" feature "brightness", "light.vintage_lampe" feature "brightness", "light.nanoleaf_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c6_helligkeit" feature "state", "sensor.esp_c3_helligkeit" feature "state", "sensor.arbeitsplatz_helligkeit" feature "state" ]
    sourceAction [ "100", "0", "0" ]
    followUpAction [ "0", "100", "0" ]
}



afterAll {
    set "light.schreibtisch_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.nanoleaf_lampe" feature "state" to "off"

    set "automation.wohnzimmer_ein" feature "state" to "on"
    set "automation.wohnzimmer_aus" feature "state" to "on"
}
