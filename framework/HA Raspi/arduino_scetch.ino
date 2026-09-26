#define PIR_PIN 4 // Pin für den AM312 PIR Sensor

unsigned long lastSensorReadTime = 0;
unsigned long lastSensorReadTimePir = 0;
int lastPirState = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
}

void loop() {
  // 1. PIR Sensor (Sofort auf 1, 10 Sekunden Verzögerung auf 0)
  int currentPirState = digitalRead(PIR_PIN);
  unsigned long currentMillis = millis();

  if (currentPirState == HIGH) {
    // Wurde neu erkannt? Sofort senden!
    if (lastPirState == LOW) {
      lastPirState = HIGH;
      Serial.print("{\"pir\":1}\n");
    }
    // Timer immer wieder zurücksetzen, solange Bewegung da ist
    lastSensorReadTimePir = currentMillis; 
  } else {
    // Keine Bewegung mehr. Sind schon 10 Sekunden vergangen?
    if (lastPirState == HIGH && (currentMillis - lastSensorReadTimePir >= 10000)) {
      lastPirState = LOW;
      Serial.print("{\"pir\":0}\n");
    }
  }
  // 2. Helligkeit (alle 1000ms)
  if (currentMillis - lastSensorReadTime >= 1000) {
    lastSensorReadTime = currentMillis;
    
    int brightness = analogRead(A0);
    // Umrechnung in Volt (Arduino misst relativ zu seinen 5V, also 1023 = 5.0V)
    float voltage = (brightness / 1023.0) * 5.0;
    
    Serial.print("{\"light\":"); Serial.print(voltage, 2); // 2 Nachkommastellen
    Serial.println("}");
  }
}
