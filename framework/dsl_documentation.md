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
**Syntax:** `precondition "SENSOR" feature "EIGENSCHAFT" equals "WERT" [skipMessage "GRUND"]`
```mt
precondition "automation.nach_sonnenuntergang" feature "state" equals "on" skipMessage "Tests erfordern, dass die Sonne untergegangen ist."
```

### 2.3. Latenzen kalibrieren (`calibrateLatency`)
Misst die Laufzeit/Latenz, die benötigt wird, bis sich der Zustand eines Aktuators beim Sensor messbar bemerkbar macht. Parameter sind optional.
```mt
calibrateLatency {
    actuator "light.schreibtisch_lampe" feature "state"
    sensor "sensor.esp_helligkeit" feature "state"
    valOff "off"
    valOn "on"
    
    // Optionale Feinabstimmung:
    minChangePercent 0.2
    toleranceFactor 1.1
    addSeconds 0
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
    
    sourceAction [ "0" ]
    followUpAction [ "100" ]
}
```

### 3.2. Verfügbare Parameter im Testblock
Je nach gewählter Metamorpher Relation benötigst du unterschiedliche Parameter. Folgende Schlüsselwörter stehen zur Verfügung:

* **Listen für Geräte:**
  * `actuators [...]`: Liste der Stellglieder.
  * `sensors [...]`: Liste der Messaufnehmer.
* **Metamorphe Testwerte:**
  * `sourceAction [...]`: Die Ausgangs-Eingabe für das System.
  * `followUpAction [...]`: Die abgewandelte Eingabe (für den Folge-Testfall).
  * `brightnessLevels [...]`: Spezifische Liste von Helligkeitswerten (falls benötigt).
* **Konfiguration & Timing:**
  * `tolerance: <Zahl>`: Erlaubte Abweichung bei Messungen.
  * `duration: <Zahl>`: Dauer einer Messung in Sekunden.
  * `waitTime: <Zahl>`: Wartezeit nach einer Aktion (wegen Pipeline-Latenzen).
* **Profile & Historische Daten:**
  * `profile: "Profilname"`: Name eines JSON-Geräteprofils (z.B. für `substitution`).
  * `historicalSamples: <Zahl>`: Anzahl der Abtastwerte (z.B. 0, 1, 2... 100).
  * `historicalFile: "Dateiname.json"`: Name der Ausgabedatei für historische Daten.

---

## 4. Vollständiges Beispiel

Hier ist ein realistisches Skript, das die Lampe kalibriert und anschließend auf Monotonie prüft (je heller die Lampe eingestellt wird, desto höher muss der gemessene Helligkeitswert des Sensors sein):

```mt
beforeAll {
    // Vorbedingung: Es muss dunkel sein
    precondition "automation.nach_sonnenuntergang" feature "state" equals "on" skipMessage "Zu hell für diesen Test!"
    
    // Setup
    set "automation.wohnzimmer_ein" feature "state" to "off"
    
    // Latenz messen
    calibrateLatency {
        actuator "light.schreibtisch_lampe" feature "state"
        sensor "sensor.esp_c3_helligkeit" feature "state"
        valOff "off"
        valOn "on"
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
    
    sourceAction [ "20" ]
    followUpAction [ "80" ]
    
    tolerance: 0.05
    waitTime: 2.0
}
```

## Ausführung und CLI-Befehle

Die DSL bringt ein Command-Line Interface (CLI) mit, um die geschriebenen `.mt`-Dateien zu validieren und in `.json`-Dateien umzuwandeln, die dann vom Test-Runner verwendet werden.

### 1. `.mt` in `.json` konvertieren

* **Alle Dateien im Verzeichnis umwandeln**:
  ```bash
  npm run generate
  ```
  Sucht alle `.mt`-Dateien im aktuellen Verzeichnis, validiert sie (zeigt Fehler bei Syntax- oder Typ-Problemen an) und generiert die zugehörigen `.json`-Dateien.

* **Spezifische Datei umwandeln**:
  ```bash
  npm run generate -- <dateiname>.mt
  ```
  Oder direkt über das CLI-Skript:
  ```bash
  node out/cli/main.js generate <dateiname>.mt
  ```

* **Ausgabeverzeichnis definieren**:
  Über das Argument `-d` oder `--destination` kannst du angeben, wo die JSON-Dateien gespeichert werden sollen:
  ```bash
  node out/cli/main.js generate <dateiname>.mt -d /pfad/zum/zielordner
  ```

### 2. Befehle zur Weiterentwicklung der DSL

Wenn du die Sprache selbst erweitern möchtest (z. B. in der Grammatik `framework/dsl/src/language/mt-dsl.langium`), stehen im `dsl`-Verzeichnis folgende Befehle zur Verfügung:

* **`npm run langium:generate`**:
  Erzeugt die Infrastruktur (Parser, AST-Typen etc.) neu, basierend auf der `.langium`-Datei. Muss nach jeder Änderung an der Grammatik ausgeführt werden.
* **`npm run build`**:
  Kompiliert den TypeScript-Code (inklusive der CLI und des VS Code Plugins).
* **`npm run build:extension`**:
  Kompiliert ausschließlich das VS Code Plugin.
* **`npm run watch`**:
  Startet einen Hintergrundprozess, der bei jeder Dateiänderung (an TypeScript oder Grammatik) automatisch neu kompiliert. Sehr nützlich während der Entwicklung.

### 3. Test-Ausführung (Python)

Nach der erfolgreichen Generierung der JSON-Dateien können die Tests über den Python-Runner ausgeführt werden:

```bash
pytest tests/test_dsl_runner.py -v --wait-time=5.0 --monitor --log
```

Einen spezifischen Test ausführen (z. B. gefiltert nach dem Namen "substitution"):
```bash
pytest tests/test_dsl_runner.py -k "substitution" -v --wait-time=5.0 --monitor --log
```

## DSL Plugin (Language Server) in VS Code starten

Das Plugin bietet Syntax-Highlighting, Autovervollständigung und Fehlerüberprüfung direkt im Editor:

1. Navigiere in den `dsl`-Ordner: `cd framework/dsl`
2. Installiere die Abhängigkeiten:
   ```bash
   npm install
   ```
3. Öffne das Projekt in VS Code und drücke **F5**. Ein neues VS Code Fenster ("Extension Development Host") öffnet sich, in dem die `.mt`-Dateien mit voller Sprachunterstützung bearbeitet werden können.



