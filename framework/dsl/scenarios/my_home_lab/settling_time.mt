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

        // --- Optionale Parameter (Müssen genau in dieser Reihenfolge stehen) ---

        // 1. Ab wieviel Prozent Änderung gegenüber Baseline (valOff) startet der Monitor?
        minChangePercent 0.01

        // 2. Maximal erlaubte Schwankung (hier 10%) innerhalb des Settle-Fensters
        maxSettleTolerance 0.01

        // 3. Multiplikator, der auf die am Ende gemessene Settle-Latenz aufgeschlagen wird
        toleranceFactor 1



        // 4. Wie viele Kalibrierungsdurchläufe?
        runs 5


        // 5. Wie groß ist das Sliding Window in dem die Sensoren sich beruhigen müssen? (in Sekunden)
        settleTime 5.0
    }


}

beforeEach {

    set "light.nanoleaf_lampe" feature "state" to "off"
    set "light.vintage_lampe" feature "state" to "off"
    set "light.schreibtisch_lampe" feature "state" to "off"


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