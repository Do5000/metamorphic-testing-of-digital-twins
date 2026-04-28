#include "DHT.h"
#include <IRremote.hpp> // Die neue Infrarot Bibliothek

#define DHTPIN 2
#define DHTTYPE DHT11
#define IR_RECEIVE_PIN 3 // Pin S deines IR-Moduls

DHT dht(DHTPIN, DHTTYPE);
unsigned long lastDHTReadTime = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); 
}

void loop() {
  // 1. Infrarot (Wird bei JEDEM Schleifendurchlauf in Millisekundenbruchteilen geprüft!)
  if (IrReceiver.decode()) {
    // Wir senden die Taste direkt als kleinen Hex-String
    String hexCode = String(IrReceiver.decodedIRData.command, HEX);
    
    if (hexCode != "0") { // 0 ignorieren (passiert bei Halten der Taste)
      Serial.print("{\"ir_btn\":\""); Serial.print(hexCode); Serial.println("\"}");
    }
    IrReceiver.resume(); // Für den nächsten Tastendruck bereit machen
  }

  // 2. Temperatursensor (Nur alle 2000ms auswerten, OHNE das Skript zu blockieren)
  unsigned long currentMillis = millis();
  if (currentMillis - lastDHTReadTime >= 2000) {
    lastDHTReadTime = currentMillis;
    
    int brightness = analogRead(A0);
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    if (!isnan(humidity) && !isnan(temperature)) {
      Serial.print("{\"light\":"); Serial.print(brightness);
      Serial.print(",\"temp\":"); Serial.print(temperature);
      Serial.print(",\"hum\":"); Serial.print(humidity);
      Serial.println("}");
    }
  }
}
