## Detailed Results Living Lab


---

### Control Adaptation

* **S1 (Monotonicity)**
  * **Goal:** Verify monotonic actuator-sensor response and uncover actuator scaling, sign inversions, or mapping faults.
  * **High Ambient Daylight (Afternoon):**
    * **Log:** [s1_living_lab_monotony_daylight_fail.log](s1_living_lab_monotony_daylight_fail.log)
    * **Result:** **32 PASSED**, **8 FAILED** (40 tests across ceiling lights and WP1 workplace sensors).
    * **Detail:** 32 tests passed with expected directional increases. All 8 failures occurred because of the described failure in lighting_control_anomalies.md
  * **Night / Low Lux & Sensor Quantization:**
    * **Log:** [s1_living_lab_monotony_night_fail.log](s1_living_lab_monotony_night_fail.log)
    * **Result:** **32 PASSED**, **8 FAILED** (40 tests in dark conditions).
    * **Detail:** 32 tests passed.All 8 failures occurred because of the described failure in lighting_control_anomalies.md
  * **Fault Injection (Actually a Fault -> WP2 not reachable):**
    * **Log:** [s1_living_lab_fault_injection_wp2_offline.log](s1_living_lab_fault_injection_wp2_offline.log)
    * **Result:** **0 PASSED**, **20 FAILED**.
    * **Test Setup for the fail:** All 4 sensor endpoints at Workplace 2 (`TSL1_LowerScreen`, `TSL2_Keyboard`, `TSL3_UpperScreen`, `TSL4_UpperScreen`) were unpowered/offline in the Digital Twin.
    * **Detail:**  Sensors returned `None`. All 20 tests across 5 iterations failed.


* **S2 (Invariance)**
  * **Goal:** Verify system invariance ($75\% \rightarrow 0\% \rightarrow 75\%$) and detect stale state, duplicate processing, or non-deterministic control behavior.
  * **Ceiling Illuminance Cyclic Test:**
    * **Log:** [s2_living_lab_invariance_ceiling_fail.log](s2_living_lab_invariance_ceiling_fail.log)
    * **Result:** **1 PASSED**, **4 FAILED** (5 iterations on `Illuminance.Room518a_Ceiling`).
    * **Detail:** 
      * *Passed Run (Iteration 5):* Digital twin responded deterministically through $75\% \rightarrow 0\% \rightarrow 75\%$. The final reading ($160.0\text{ lx}$) matched the initial baseline ($160.0\text{ lx}$, difference $0.0 \le 3.2\text{ lx}$ within 2% tolerance).
      * *Automatic ~10s Shutoff (Iterations 2 & 4):* Luminaires turned on ($142\text{ lx}$ and $160\text{ lx}$), held for 10 seconds, and turned themselves off at $t = 21–22\text{s}$ ($0.83\text{ lx}$), failing with $0.83$ vs. $160.83\text{ lx}$.
      * *Zero Response (Iteration 1):* The Phase 3 re-actuation command produced no physical light; the sensor flatlined at $0.83\text{ lx}$ throughout all 24 seconds ($0.83$ vs. $129.17\text{ lx}$).
      * *Settling Drift (Iteration 3):* Minor illuminance variation ($159.17$ vs. $155.0\text{ lx}$, $\Delta = 4.17 > 3.18\text{ lx}$ allowed).


* **S3 (Conservation)**
  * **Goal:** Verify conservation of aggregate illuminance across complementary luminaire configurations summing to 100% (`norden_tuer` and `sueden_tuer`).
  * **Multi-Ratio Complementary Dimming (65/35, 75/25, 90/10, 100/0):**
    * **Log:** [s3_living_lab_conservation_fail.log](s3_living_lab_conservation_fail.log)
    * **Result:** **10 PASSED**, **10 FAILED** (20 tests across 4 ratios over 5 repetitions each).
    * **Detail:**
      * *Balanced Split (65/35):* **5 PASSED, 0 FAILED (100% pass rate).** Measured illuminance remained within tolerance across all 5 runs ($21.67$ vs. $22.5\text{ lx}$, $\Delta \le 1.25\text{ lx}$). Symmetrically blended fields compensate for spatial distances.
      * *Moderately Asymmetric Split (75/25):* 2 PASSED, 3 FAILED. Failures occurred in iterations 3–5 because Phase 1 (`norden_tuer = 0.75`) failed to actuate (24s flatline at $0.83\text{ lx}$), while Phase 2 turned on to $30.0\text{ lx}$.
      * *High Asymmetry Split (90/10):* 3 PASSED, 2 FAILED. Marginal threshold exceedances caused by geometric displacement between the sensor and individual luminaires ($22.5$ vs. $25.0\text{ lx}$).
      * *Extreme Split (100/0):* 0 PASSED, 5 FAILED. All 5 runs failed due to the ~10s automatic shutoff during follow-up actuation ($100\%$ on `sueden_tuer`), dropping back to $0.83\text{ lx}$ at query time.

---

### Spatial Interactions & Isolation

* **S5 (Cross-Workplace Isolation)**
  * **Goal:** Validate cross-workplace isolation and spatial independence between Workplace 1 and Workplace 2.
  * **Isolation Check with Workplace 2 Offline:**
    * **Log:** [s5_living_lab_cross_workplace_wp2_offline_failed.log](s5_living_lab_cross_workplace_wp2_offline_failed.log)
    * **Result:** **0 PASSED**, **10 FAILED** (5 iterations for window and door luminaire actuation).
    * **Detail:** All 10 tests failed with `AssertionError: Sensor 'TSL2_Keyboard_spec.Room518a_WP2' returned None during source test case`. Confirms that spatial isolation relations correctly abort when the monitoring endpoint of the adjacent workspace is disconnected.

---

### Environmental Dynamics

* **S8 (Natural Daylight Robustness - 30 Cycles)**
  * **Goal:** Verify consistency of metamorphic relations under changing natural daylight conditions across 30 consecutive execution cycles of 6 metamorphic properties.
  * **30-Cycle Robustness Run:**
    * **Log:** [s8_living_lab_30cycles.log](s8_living_lab_30cycles.log)
    * **Result:** **136 PASSED**, **44 FAILED** (180 tests total, **75.6% pass rate**).
    * **Detail by Relation:**
      * `TC_S8_Monotony`: **28 PASSED**, 2 FAILED (**93.3%**). 
      * `TC_S8_Invariance`: **26 PASSED**, 4 FAILED (**86.7%**). 
      * `TC_S8_Conservation_65` (65/35): **28 PASSED**, 2 FAILED (**93.3%**). 
      * `TC_S8_Conservation_75` (75/25): **24 PASSED**, 6 FAILED (**80.0%**).
      * `TC_S8_Conservation_90` (90/10): **16 PASSED**, 14 FAILED (**53.3%**).
      * `TC_S8_Conservation_100` (100/0): **14 PASSED**, 16 FAILED (**46.7%**).
    * **Physical Finding:** While the Home Lab (small window) achieved 100% pass (180/180), the Living Lab experienced afternoon ambient solar drift between $215\text{ lx}$ and $640\text{ lx}$. This empirically proves that balanced dimming splits (65/35) withstand dynamic daylight drift, while extreme single-lamp shifts (100/0) are vulnerable to ambient solar changes between test states.

---

### Multi-Scenario Benchmark

* **Full Suite Morning Benchmark (S1–S8)**
  * **Goal:** Comprehensive validation run across all metamorphic properties under moderate morning daylight after system reconnection.
  * **Morning Integration Run:**
    * **Log:** [suite_living_lab_multi_scenario_morning_benchmark.log](suite_living_lab_multi_scenario_morning_benchmark.log)
    * **Result:** **18 PASSED**, **8 FAILED** (26 tests total, **69.2% pass rate**).
    * **Detail:**
      * *Passed (18 tests):* S1 Monotonicity (all 5 ceiling light configurations), S2 Invariance, S3 Conservation (balanced ratios), S4 Registration and addressability, and S8 baseline relations passed without issue.
      * *Failures (8 tests):* 3 failures caused by offline WP2 sensors (`returned None`), 1 failure in S2 due to morning solar baseline drift ($408.33$ vs. $394.17\text{ lx}$), 3 failures in S5 proportionality due to sensor geometric orientation discrepancies (keyboard vs. monitor shadow), and 1 failure in S7 stability due to 60s sunlight fluctuation ($53.33\text{ lx}$ fluctuation $> 18.67\text{ lx}$ allowed).
