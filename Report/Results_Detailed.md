## Detailed Results per Scenario

The following is a detailed, scenario-by-scenario breakdown of the metamorphic testing results (S1–S10), focusing on the numerical outcomes and specific failure reasons.

Picture of the test setup: [home_lab.pdf](home_lab.pdf)

### Control Adaptation
* **S1 (Monotonicity)**
  * **Goal:** Check monotonicity and reveal scaling, sign, or device-mapping faults.
  * **2% Tolerance:**
    * **Log:** [s1_2%.log](reports_final/s1_2%25.log)
    * **Result:** **10 PASSED**, 0 FAILED.
    * **Detail:** Monotonicity correctly held in all cases. No mapping faults detected.
    
  *  **5% Tolerance:**
      * **Log:** [s1_5%.log](reports_final/s1_5%.log)
      * **Result:** **5 PASSED**, 5 FAILED.
      * **Detail:** Only half of the Tests PASSED (brightness change from 0 to 100), change from 20 to 80, a tolerance from 5% is too big.
  *  **Fault injection (sensor is not connected = stuck value)**
      * **Log:** [s1_2%_fault.log](reports_final/s1_2%25_fault.log)
      * **Result:** **0 PASSED**, 10 FAILED.
      * **Detail:** Fault injection shows, that stuck sensors can be detected.



* **S2 (Invariance)**
  * **Goal:** Check invariance and reveal stale state, duplicate processing, or non-deterministic behavior.
  * **Test on DT without fault injection**
    * **Log:** [s2.log](reports_final/s2.log)
    * **Result:** **5 PASSED**, 0 FAILED.
    * **Detail:** The DT responded deterministically. No failure states were found.
  * **with fault injection**
    * **Log:** [s2_fault.log](reports_final/s2_fault.log)
    * **Result:** **0 PASSED**, 5 FAILED.
    * **Detail:** Fault injection shows, that stuck sensors can be detected.


* **S3 (Conservation)**
  * **Goal:** Check conservation of aggregate illuminance.
  * **Test on DT without fault injection**
    * **Log:** [s3_passed_vintage_lampe_nahe.log](reports_final/s3_passed_vintage_lampe_nahe.log)
    * **Result:** **20 PASSED**, **0 FAILED**.
    * **Detail:** measured brightness on sensor stays in 5% tolerance in every light configuration (100/0; 90/10; 75/25; 65/35)
  * **with fault injection (shifted one light source away from the sensor)**
    * **Log:** [s3_fault.log](reports_final/s3_fault.log)
    * **Result:** **15 PASSED**, **5 FAILED**.
    * **Detail:** light configuration 100/0 failed


### Model / Device Evolution
* **S4 (Integrate additional luminaire)**
  * **Goal:** Check successful registration, addressability, and local response (monotony and invariance relation).
  * **Check successful registration, addressability, and local response only.**
    * **Log:** [s4_without_conservation.log](reports_final/s4_without_conservation.log)
    * **Result:** **10 PASSED, 0 FAILED**
    * **Detail:** Shows that the new luminare response correctly.
  * **with Conservation**
    * **Log:** [s4_with_conservation.log](reports_final/s4_with_conservation.log)
    * **Result:** 10 PASSED, 20 FAILED
    * **Detail:** 20 Conservation Tests failed intentionally, because new luminare (nanoleaf_lampe) don't replace an existing(like schreibtisch_lampe), instead it is an additionally luminare, further away => conservation fails

* **S5 (Cross-workplace / Integrate additional sensor )**
  * **Goal:** Check correct spatial binding, consistency, and cross-workplace interference.
  * **Result (Cross-Workplace without wall):** 0 PASSED, **10 FAILED**.
    * **Log:** [s5_cross-workplace_without_wall.log](reports_final/s5_cross-workplace_without_wall.log)
    * **Detail:** A `not proportionality` relation was defined to ensure a luminaire doesn't affect an unrelated workspace. All 10 tests failed because they *were* proportional, revealing significant light leakage across workspaces.
  * **Result (Cross-Workplace with wall):** 10 PASSED, **0 FAILED**.
    * **Log:** [s5_cross-workplace_with_wall.log](reports_final/s5_cross-workplace_with_wall.log)
    * **Detail:** A `not proportionality` relation was defined to ensure a luminaire doesn't affect an unrelated workspace. All 10 tests passed because they were *not* proportional, because of a "wall" between the two workplaces to block the light.
  
  * **Result (Proportionality bounds / additional sensor ):** 10 PASSED, **5 FAILED**.
    * **Log:** [s5_prop_failed3.log](reports_final/s5_prop_failed.log)
    * **Detail:** 5 tests violated the strict 5% tolerance, with observed percentage changes deviating by over 80%. These failures occurred exclusively in `TC_S5_Proportionality_100`, which tests the transition from a completely off state (0%) to fully on (100%). Explanation??

* **S6 (Replace existing sensor)**
  * **Goal:** Check DT preservation of device semantics and consistent relations after replacement.
  * **Log:** [s6.log](reports_final/s6.log)
  * **Result:** 30 PASSED, **0 FAILED**.
  * **Detail:** esp_c6_helligkeit sensor got replaced and passed all 30 Tests, similar to the S1, S2 and S3 tests.

### Timing and Context
* **S7 (Observe pipeline latency)**
  * **Goal:** Measure the latency between issuing an input command and detecting the corresponding change at the sensor.
  * **Log:** [s7.log](reports_final/s7.log)
  * **Result Settling Time:** 
    * [SUCCESS] sensor.esp_c6_helligkeit (state): 2.192s
    * [SUCCESS] sensor.esp_c3_helligkeit (state): 3.030s
    * [SUCCESS] sensor.arbeitsplatz_helligkeit (state): 2.004s
  * **Result Initial change** 
    * [SUCCESS] sensor.esp_c6_helligkeit (state): 1.327s
    * [SUCCESS] sensor.esp_c3_helligkeit (state): 2.379s
    * [SUCCESS] sensor.arbeitsplatz_helligkeit (state): 1.008s
  * **Result Stability:** 1 PASSED, **0 FAILED**.
  * **Detail:** The stability test passed due to sufficient wait time for sensor settling.


* **S8 (Different daylight conditions)**
  * **Goal:** Check relative relation consistency under changing daylight.
  * **Log:** [s8.log](reports_final/s8.log)
  * **Result:** **180 PASSED**, **0 FAILED**.
  * **Detail:** relations held robustly for 30 repetitions under changing daylight

### Environmental Variation
* **S9 (Toggle occupancy input)**
  * **Goal:** Check consistent control behavior and reveal state-transition faults.
  * **Log:** [s9_precence_live_passed.log](reports_final/s9_precence_live_passed.log), [s9_presence_live_skipped.log](reports_final/s9_presence_live_skipped.log)
  * **Result:** **1 PASSED**, 0 FAILED, **1 SKIPPED**.
  * **Detail:** One test was intentionally skipped because a precondition correctly detected that the room was currently occupied. Second test passed the precondition (nobody was in the room)

* **S10 (Observe sensor over continuous period)**
  * **Goal:** Check reading stability and reveal sensor drift.
  * **200sec**
    * **Log:** [s10_stability_200.log](reports_final/s10_stability_200.log)
    * **Result:** **10 PASSED**, 0 FAILED.
    * **Detail:** Sensor readings remained stable and variance was within acceptable noise margins (5%) over the tested time (200 seconds).
  * **3hours**
    * **Log:** [s10_fail.log](reports_final/s10_fail.log)
    * **Result:** **0 PASSED**, **1 FAILED**
    * **Detail:** The Test failed, because of a value jump in the beginning of the Test (maybe light from outside), but the remaining hours, there was no sensor drift. ![s10_fail_chart.png](reports_final/s10_fail_chart.png)