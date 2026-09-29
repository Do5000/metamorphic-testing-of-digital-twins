## Detailed Results per Scenario

The following is a detailed, scenario-by-scenario breakdown of the metamorphic testing results (S1–S10), focusing on the numerical outcomes and specific failure reasons.

Picture of the test setup: [home_lab.pdf](home_lab.pdf)

### Control Adaptation
* **S1 (Monotonicity)**
  * **Goal:** Check monotonicity and reveal scaling, sign, or device-mapping faults.
  * **Log:** [s1_monotony.log](reports_final/s1_monotony.log)
  * **Result:** **20 PASSED**, 0 FAILED.
  * **Detail:** Monotonicity correctly held in all cases. No mapping faults detected.

* **S2 (Invariance)**
  * **Goal:** Check invariance and reveal stale state, duplicate processing, or non-deterministic behavior.
  * **Log:** [s2_invariance.log](reports_final/s2_invariance.log)
  * **Result:** **5 PASSED**, 0 FAILED.
  * **Detail:** The DT responded deterministically. No failure states were found.

* **S3 (Conservation)**
  * **Goal:** Check conservation of aggregate illuminance.
  * **Log:** [s3_conservation.log](reports_final/s3_conservation.log)
  * **Result:** **15 PASSED**, **5 FAILED**.
  * **Detail:** 5 tests failed (Explanation in S8)

### Model / Device Evolution
* **S4 (Integrate additional luminaire)**
  * **Goal:** Check successful registration, addressability, and local response.
  * **Result:** **No tests available.**
  * **Detail:** Same test like S1.

* **S5 (Cross-workplace / Integrate additional sensor )**
  * **Goal:** Check correct spatial binding, consistency, and cross-workplace interference.
  * **Result (Cross-Workplace):** 0 PASSED, **10 FAILED**.
    * **Log:** [s5_cross-workplace_daylight.log](reports_final/s5_cross-workplace_daylight.log)
    * **Detail:** A `not proportionality` relation was defined to ensure a luminaire doesn't affect an unrelated workspace. All 10 tests failed because they *were* proportional, revealing significant light leakage across workspaces.
  * **Result (Proportionality bounds / additional sensor ):** 10 PASSED, **5 FAILED**.
    * **Log:** [s5_proportionality.log](reports_final/s5_proportionality.log)
    * **Detail:** 5 tests violated the strict 5% tolerance, with observed percentage changes deviating by 11% to 13%. These failures occurred exclusively in `TC_S5_Proportionality_100`, which tests the transition from a completely off state (0%) to fully on (100%). Explanation??

* **S6 (Replace existing sensor)**
  * **Goal:** Check DT preservation of device semantics and consistent relations after replacement.
  * **Result:** 30 PASSED, **5 FAILED**.
  * **Detail:** Interface rebinding succeeded, and while 5 conservation tests failed, this is actually the expected behavior. The original sensor also failed these same conservation tests (e.g., `TC_S8_Conservation_100`, which is analogous to `TC_S6_Conservation_100`), demonstrating that the replaced sensor accurately preserves the original device semantics.

### Timing and Context
* **S7 (Observe pipeline latency)**
  * **Goal:** Measure the latency between issuing an input command and detecting the corresponding change at the sensor.
  * **Log:** [s7_pipeline_latency_stability.log](reports_final/s7_pipeline_latency_stability.log)
  * **Result Latency:** min: 0.399s; max: 0.991s; mean: 0.715s
  * **Result Stability:** 0 PASSED, **5 FAILED**.
  * **Detail:** The 5 stability tests failed due to insufficient wait time for sensor settling, rather than actual fluctuations in the sensor readings. For this scenario, these stability failures are negligible, as the primary objective was to measure the pipeline latency.

* **S8 (Different daylight conditions)**
  * **Goal:** Check relative relation consistency under changing daylight.
  * **Log:** [s8_combi_twilight.log](reports_final/s8_combi_twilight.log)
  * **Result:** **119 PASSED**, **21 FAILED**.
  * **Detail:** Relative relations held robustly for most cases, but 21 conservation tests failed. Of these, 20 failures occurred in `TC_S8_Conservation_100`. This suggests that when one light is completely off, the sensor measures a noticeably different value. Possible reasons include the sensor's imperfect measurement of spectral illuminance, differing incidence angles from the two light sources, or non-linear brightness curves of the bulbs (i.e., they are disproportionately brighter at lower dimming levels). The single remaining failure occurred in `TC_S8_Conservation_90` during the final trial of 20 repetitions, likely caused by interference from the sun shining at a low angle.

### Environmental Variation
* **S9 (Toggle occupancy input)**
  * **Goal:** Check consistent control behavior and reveal state-transition faults.
  * **Log:** [s9_precence_live_passed.log](reports_final/s9_precence_live_passed.log), [s9_presence_live_skipped.log](reports_final/s9_presence_live_skipped.log)
  * **Result:** **1 PASSED**, 0 FAILED, **1 SKIPPED**.
  * **Detail:** One test was intentionally skipped because a precondition correctly detected that the room was currently occupied. Second test passed the precondition (nobody was in the room)

* **S10 (Observe sensor over continuous period)**
  * **Goal:** Check reading stability and reveal sensor drift.
  * **Log:** [s10_stability.log](reports_final/s10_stability.log)
  * **Result:** **10 PASSED**, 0 FAILED.
  * **Detail:** Sensor readings remained stable and variance was within acceptable noise margins (5%) over the tested time (200 seconds).
