# Dokumentation zur Metamorphic Testing DSL

Dieses Dokument dient als Einstieg für Anwender der MT-DSL. Die DSL (Domain-Specific Language) wurde entwickelt, um metamorphes Testen für Digitale Zwillinge (Digital Twins) und Smart-Home-Szenarien einfach, lesbar und standardisiert zu definieren.

Dateien dieser Sprache verwenden die Dateiendung **`.mt`**.

---

## 1. Grundstruktur einer `.mt`-Datei

Eine `.mt`-Datei besteht in der Regel aus zwei Bausteinen:
1. **Lifecycle-Hooks** (z. B. `beforeAll`, `beforeEach`): Hier definierst du, was vor oder nach den Tests passieren soll (z.B. Geräte in einen definierten Grundzustand versetzen oder Latenzen kalibrieren).
2. **Test-Definitionen** (`test`): Hier wird der eigentliche metamorphe Test konfiguriert.

Ein typischer Ablauf sieht so aus:
```mt
beforeAll {
    // Setup für alle Tests
}

beforeEach {
    // Setup vor jedem einzelnen Test
}

test "mein_erster_test" {
    // Testkonfiguration
}
```

---

## 2. Lifecycle-Hooks und Befehle

Du kannst vier verschiedene Hooks verwenden:
- `beforeAll`: Wird **einmal** vor allen Tests ausgeführt.
- `afterAll`: Wird **einmal** nach allen Tests ausgeführt.
- `beforeEach`: Wird **vor jedem** Test ausgeführt.
- `afterEach`: Wird **nach jedem** Test ausgeführt.

Innerhalb dieser Blöcke stehen dir drei Arten von Befehlen (Statements) zur Verfügung:

### 2.1. Zustand setzen (`set`)
Ändert den Zustand eines Geräts (Aktuators).
**Syntax:** `set "GERÄT" feature "EIGENSCHAFT" to "WERT"`
```mt
set "light.schreibtisch_lampe" feature "state" to "off"
set "switch.fernseher" feature "state" to "on"
```

### 2.2. Vorbedingungen prüfen (`precondition`)
Pausiert oder überspringt Tests, falls eine bestimmte Bedingung in der physischen Umgebung nicht erfüllt ist.
**Syntax:** `precondition "SENSOR" feature "EIGENSCHAFT" equals "WERT" [skip_message "GRUND"]`
```mt
precondition "automation.nach_sonnenuntergang" feature "state" equals "on" skip_message "Tests erfordern, dass die Sonne untergegangen ist."
```

### 2.3. Latenzen kalibrieren (`calibrate_latency`)
Misst die Laufzeit/Latenz, die benötigt wird, bis sich der Zustand eines Aktuators beim Sensor messbar bemerkbar macht. Parameter sind optional.
```mt
calibrate_latency {
    actuator "light.schreibtisch_lampe" feature "state"
    sensor "sensor.esp_helligkeit" feature "state"
    val_off "off"
    val_on "on"
    
    // Optionale Feinabstimmung:
    min_change_percent 0.2
    tolerance_factor 1.1
    add_seconds 0
    timeout 3.0
    runs 1
}
```

---

## 3. Einen Test definieren (`test`)

Die Test-Definition beschreibt, welche *Metamorphe Relation* geprüft werden soll und welche Geräte dafür verwendet werden.

**Syntax:**
```mt
test "Test_Name" {
    relation: <Relation>
    ... Parameter ...
}
```

### 3.1. Relationen und Pflichtparameter
Jeder Test benötigt eine **`relation`**. Mögliche Relationen sind beispielsweise `monotonicity`, `invariance`, `substitution` etc.
Zudem musst du meist Aktuatoren und Sensoren als Listen (`[...]`) übergeben:
```mt
test "test_home_monotony" {
    relation: monotonicity
    
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_helligkeit" feature "state" ]
    
    source_action [ "0" ]
    followup_action [ "100" ]
}
```

### 3.2. Verfügbare Parameter im Testblock
Je nach gewählter Metamorpher Relation benötigst du unterschiedliche Parameter. Folgende Schlüsselwörter stehen zur Verfügung:

* **Listen für Geräte:**
  * `actuators [...]`: Liste der Stellglieder.
  * `sensors [...]`: Liste der Messaufnehmer.
* **Metamorphe Testwerte:**
  * `source_action [...]`: Die Ausgangs-Eingabe für das System.
  * `followup_action [...]`: Die abgewandelte Eingabe (für den Folge-Testfall).
  * `brightness_levels [...]`: Spezifische Liste von Helligkeitswerten (falls benötigt).
* **Konfiguration & Timing:**
  * `tolerance: <Zahl>`: Erlaubte Abweichung bei Messungen.
  * `duration: <Zahl>`: Dauer einer Messung in Sekunden.
  * `wait_time: <Zahl>`: Wartezeit nach einer Aktion (wegen Pipeline-Latenzen).
* **Profile & Historische Daten:**
  * `profile: "Profilname"`: Name eines JSON-Geräteprofils (z.B. für `substitution`).
  * `historical_samples: <Zahl>`: Anzahl der Abtastwerte (z.B. 0, 1, 2... 100).
  * `historical_file: "Dateiname.json"`: Name der Ausgabedatei für historische Daten.

---

## 4. Vollständiges Beispiel

Hier ist ein realistisches Skript, das die Lampe kalibriert und anschließend auf Monotonie prüft (je heller die Lampe eingestellt wird, desto höher muss der gemessene Helligkeitswert des Sensors sein):

```mt
beforeAll {
    // Vorbedingung: Es muss dunkel sein
    precondition "automation.nach_sonnenuntergang" feature "state" equals "on" skip_message "Zu hell für diesen Test!"
    
    // Setup
    set "automation.wohnzimmer_ein" feature "state" to "off"
    
    // Latenz messen
    calibrate_latency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        val_off "off"
        val_on "on"
        runs 1
    }
    
    // Lampe wieder ausschalten
    set "light.schreibtisch_lampe" feature "state" to "off"
}

beforeEach {
    // Vor jedem einzelnen Testlauf Störfaktoren ausschalten
    set "switch.fernseher_steckdose" feature "state" to "off"
}

test "TC_01_Monotony_DeskLight" {
    relation: monotonicity
    
    actuators [ "light.schreibtisch_lampe" feature "brightness" ]
    sensors [ "sensor.esp_c3_helligkeit" feature "state" ]
    
    source_action [ "20" ]
    followup_action [ "80" ]
    
    tolerance: 0.05
    wait_time: 2.0
}
```

## Ausführung

Von .mt zu .json:

```
npm run generate
```

Test/Tests ausführen:

```
pytest tests/test_dsl_runner.py -v --wait-time=5.0 --monitor --log
```

```
pytest tests/test_dsl_runner.py -k "substitution" -v --wait-time=5.0 --monitor --log
```

## DSL Plugin starten

```
npm install
```

Taste F5


