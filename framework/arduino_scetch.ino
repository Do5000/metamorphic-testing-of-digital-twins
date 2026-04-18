#include "DHT.h"

// Definieren des DHT11 Pins und Typs
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  int brightness = analogRead(A0);
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  
  // Wenn der Sensor nicht antwortet, sende nichts (sonst stürzt das Python Skript drüben ab)
  if (!isnan(humidity) && !isnan(temperature)) {
    // Sende die Daten extrem clever als sauberen JSON-String über das USB-Kabel:
    Serial.print("{\"light\":"); Serial.print(brightness);
    Serial.print(",\"temp\":"); Serial.print(temperature);
    Serial.print(",\"hum\":"); Serial.print(humidity);
    Serial.println("}");
  }
  
  // WICHTIG: DHT11 Sensoren verlangen zwingend mindestens 2 Sekunden Pause zwischen Messungen!
  delay(2000);
}


