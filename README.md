# Metamorphic Testing

## Relations:



## 1. Monotonicity
- **The concept:** If I increase the input, the output must not decrease.
- **Example in the Living Lab:**  
  You send the command to make the lamp brighter (input: setpoint is increased).  
  The light sensor in the room (output: illuminance) must now measure a value that is equal to or higher than before. It must not decrease.

## 2. Invariance
- **The concept:** Under stable conditions, the same input should lead to the same output (or at least a very similar one).
- **Example in the Living Lab:**  
  If you set 500 lux today and again 500 lux tomorrow (with the same daylight conditions), the sensor should measure the same value.  
  Even if you add new sensors, the behavior of the existing system must not suddenly change.

## 3. Conservation 
- **The concept:** If inputs are changed in such a way that the total amount of energy remains the same, the overall output should also remain comparable.
- **Example in the Living Lab:**  
  You have two lamps. You dim lamp A by 10% and increase lamp B by a corresponding amount.  
  The measured overall brightness in the room (sum of the sensors) should remain approximately the same.

## 4. Permutation (Permutative Relation)
- **The concept:** Changing the order of input values should not change the final result (for certain operations).
- **Example in the Living Lab:**  
  You send commands to multiple lamps in the room.  
  Whether you turn on lamp A first and then lamp B, or lamp B first and then lamp A, the final result (the measured total brightness in the room) must be identical.


## 5. Inclusion (Inclusive Relation)
- **The concept:** The result of a computation on a subset must be consistent with the result on the complete set (e.g., the complete set must contain the results of the subset or be greater than or equal in value).
- **Example in the Living Lab:**  
  You query the energy consumption.  
  The energy consumption of the entire Living Lab (parent) must always be greater than or equal to the sum of the energy consumption of individual workstations (children).


## 6. Inversion (Invertive Relation)
- **The concept:** Applying a function and then its inverse function should restore the original state.
- **Example in the Living Lab:**  
  Control of blinds or lighting.  
  If you increase the light by 50% and then decrease it by 50%, the sensor value should return (approximately) to the original value.  
  This is important for detecting hysteresis effects or state drift in the Digital Twin.

## 7. Composition (Composition of Relations – CMR)
- **The concept:** Two or more relations are combined such that the output of one relation becomes the input of the next.
- **Example in the Living Lab:**  
  You can combine permutation and monotonicity:  
  Change the order of lamp activation (permutation) **and** increase the brightness (monotonicity).  
  The output must still increase.

## 8. Additivity (Additive Relation)
- **The concept:** The result of a function applied to the sum of two inputs equals the sum of the results of the individual inputs  
  *(f(a + b) = f(a) + f(b))*.
- **Example in the Living Lab:**  
  This property only partially applies physically for light (due to light superposition), but it can apply to energy consumption.  
  The measured power consumption when lamp A and lamp B are on at the same time should equal the sum of the consumption measured when each lamp is operated individually.

## 9. Inklusions- und Teilmengen-Relationen (Datenbank-Logik)

Diese sind besonders für die IoT-Datenverarbeitung im DT relevant.

Abfrage-Inklusion: Wenn du die Durchschnittstemperatur für das ganze Gebäude abfragst, muss der Datensatz alle Werte enthalten, die auch in einer Abfrage für nur einzelne Stockwerke erscheinen.

Sensor-Redundanz: Wenn ein DT Daten von 10 Temperatursensoren in einer Halle mittelt, darf das Entfernen eines einzelnen Sensors den Mittelwert nur innerhalb eines statistisch erwartbaren Rahmens verändern; die Richtung der Änderung muss plausibel zur Messung des entfernten Sensors sein.

## 10. Statistische Metamorphe Relationen (Noise Robustness)
Problem: Sensoren rauschen. Ein absolut exakter Vergleich (==) schlägt oft fehl.
Feature: Unterstützung für Relationen wie approximately_equal oder mean_invariant. Man prüft nicht einen Einzelwert, sondern ob der Mittelwert über 10 Sekunden stabil bleibt. Das macht MT im IoT-Bereich erst praxistauglich.
