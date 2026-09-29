# Evaluation Question 1 (EQ1): Reachability and Stability

**Zielsetzung (EQ1):** Es soll evaluiert werden, ob alle konfigurierten Sensoren und Aktuatoren im Digital Twin korrekt registriert sind, ob sie über die Middleware verlässlich erreichbar sind und ob die erfassten Sensordaten über die Zeit stabil bleiben (kein Sensor-Drift). 

Um diese Forschungsfrage umfassend zu beantworten, werden die Ergebnisse der Szenarien **S8, S4, S5, S7 und S10** herangezogen.

---

## 1. Überprüfung der Sensor-Reaktivität (S8: Kombination aus S1, S2, S3)
Das Szenario S8 ist ein kombiniertes Testszenario und prüft die grundlegende Erreichbarkeit und Funktionalität (Registration & Reachability).

**Monotony & Inverted Monotony (Ergebnisse: Alle Tests PASSED)**  
Um nachzuweisen, dass Sensoren und Aktuatoren korrekt registriert sind und kontinuierlich Werte liefern, reicht ein einfacher `Monotonicity`-Test (steigender Input $\rightarrow$ steigender oder gleichbleibender Output) nicht aus. 
* **Das Problem des "Stuck Sensors":** Wenn ein Sensorwert in der Datenbank "eingefroren" ist (stuck), würde ein regulärer Monotonie-Test dennoch ein positives Ergebnis (`PASSED`) liefern, da die Bedingung "größer oder gleich" erfüllt bleibt. Alle darauffolgenden Metamorphic Relations (Invariance, Conservation, Stability) würden auf Basis dieses eingefrorenen Werts ebenfalls fehlerhafte, aber scheinbar positive Ergebnisse (Nonsens-Ergebnisse) produzieren. 
* **Die Lösung:** Durch die Ergänzung von **Inverted Monotonicity** (z. B. strikte Abnahme des Sensorwerts bei Reduzierung der Helligkeit) wird erzwungen, dass der Sensor tatsächlich auf Veränderungen reagiert. Zwar könnte theoretisch auch die `Proportionality`-Relation eingefrorene Sensoren im Abgleich mit Nachbarsensoren erkennen, jedoch schlägt dies fehl, wenn die Nachbarsensoren durch ein generelles Netzwerk- oder Middleware-Problem ebenfalls eingefroren sind.

**Conservation (Ergebnisse: Teilweise PASSED, 100/0 FAILED)**  
Unter einer Toleranz von 5 % wurden verschiedene Helligkeits-Konfigurationen (Verteilung der Set-Points auf zwei Lampen) getestet:
* **90/10, 75/25, 65/35:** Alle PASSED
* **100/0:** FAILED

*Erklärungsansätze für das Fehlschlagen bei 100/0:*
1. **Spektrale Ausleuchtung:** Wenn eine Lampe komplett ausgeschaltet ist (0%), unterscheidet sich die Lichtverteilung im Raum physikalisch maßgeblich von einer Konfiguration, bei der zwei Lampen gedimmt leuchten. Der Sensor erfasst keine perfekte, omnidirektionale spektrale Beleuchtungsstärke.
2. **Nicht-lineare Skalierung:** Die verbauten Leuchtmittel weisen keine perfekt lineare Skalierung zwischen 0 % und 100 % auf. Insbesondere im sehr niedrigen Dimm-Bereich hat eine Änderung am Set-Point überproportionale Auswirkungen auf die tatsächliche Lichtausbeute, was bei der strikten 5%-Toleranzgrenze zu einem *Fail* führt.

---

## 2. Einführung neuer Hardware-Komponenten (S4 & S5)
Um zu prüfen, ob das System auch bei Änderungen der Konfiguration erreichbar und stabil bleibt, wurden zur Laufzeit neue Komponenten eingeführt:

* **S4 (Neuer Aktuator):** Bei der Integration einer neuen Lampe (Vintage Lampe) werden analog zu S8 Kombinationen aus S1 (Monotony), S2 (Invariance) und S3 (Conservation) durchlaufen. Dies weist nach, dass der neue Aktuator im Digital Twin umgehend korrekt registriert und steuerbar ist.
* **S5 (Neuer Sensor):** Hierbei wird die `Proportionality`-Relation angewandt. Es wird unter einer Toleranz von 5 % überprüft, ob der neu hinzugefügte Sensor im Vergleich zu seinen physischen Nachbarsensoren ähnliche und logisch konsistente Werte liefert.

---

## 3. Analyse der Kommunikationslatenz (S7)
Für die Validierung der Middleware-Erreichbarkeit (Communication Latency) ermittelt S7 empirisch die Latenzen zwischen Steuerbefehl und stabiler Sensorantwort:

* **[SUCCESS]** `light.schreibtisch_lampe` $\rightarrow$ `sensor.esp_c6_helligkeit`: **0.823s**
* **[SUCCESS]** `light.schreibtisch_lampe` $\rightarrow$ `sensor.esp_c3_helligkeit`: **0.485s**
* **[SUCCESS]** `light.nanoleaf_lampe` $\rightarrow$ `sensor.esp_c6_helligkeit`: **0.526s**
* **[SUCCESS]** `light.nanoleaf_lampe` $\rightarrow$ `sensor.esp_c3_helligkeit`: **0.464s**

Die Latenzen liegen durchgängig unter einer Sekunde. Dies beweist, dass Befehle ohne signifikanten Overhead verarbeitet werden und die Aktuatoren zuverlässig erreichbar sind.

---

## 4. Langzeitstabilität und Sensor-Drift (S10)
Um sicherzustellen, dass die registrierten Sensoren auch über die Zeit hinweg verlässliche Daten liefern, wurde in S10 die Stabilität über einen Zeitraum von 200 Sekunden unter konstanten Umgebungsbedingungen getestet.

* **Resultat:** `[MR CHECK] Stability PASSED`
* **Details:** Max: 2.451, Min: 2.415
* **Auswertung:** Die Schwankung (*Fluctuation diff*) betrug lediglich **0.036**. Dies liegt weit unter der erlaubten Fehlertoleranz von 5.0 % (entspricht 0.123). 

**Fazit:** Die Sensoren weisen keinen messbaren zeitlichen Drift auf. Das Signal-Rauschen liegt auf einem extrem niedrigen Niveau, was eine sehr hohe Stabilität der Messdaten im Digital Twin bestätigt.
