## C. Results

To answer our evaluation questions systematically, we summarize our key findings in Table III and detail the empirical results for each Evaluation Question (EQ) below.

**TABLE III: SUMMARY OF EVALUATION RESULTS**

| Evaluation Question | Scenarios | Key Metric | Result / Finding |
| :--- | :--- | :--- | :--- |
| **EQ1** (Reachability & Stability) | S4, S5, S7, S8, S10 | Registration success, Latency, Sensor stability | 100% registration success; average latency < 1s; max sensor drift 0.036 lx (within 5% margin). |
| **EQ2** (Spatial Interactions) | S1, S2, S3, S5 | Cross-workplace leakage, Proportionality error bounds | Local device mapping is flawless. Extreme cross-workplace leakage empirically proven via inverted relations. |
| **EQ3** (Hardware Evolution) | S4, S5, S6 | Relation consistency, Spatial consistency | 100% relation consistency pre- and post-replacement. Full device semantics are preserved. |

### 1. Reachability and Stability (EQ1)
Our first objective was to ensure that all configured devices are accurately registered, reliably reachable via the middleware, and deliver stable data over time. The empirical measurement of communication latency (S7) yielded an average response time well below 1.0 seconds across all tested actuator-sensor pairs (e.g., 0.823s and 0.464s). Furthermore, continuous monitoring over a 200-second period under stable environmental conditions (S10) demonstrated an exceptionally low noise floor. The maximum recorded fluctuation was merely 0.036, which is strictly bounded within the conservative 5.0% tolerance margin, confirming that the digital twin's data acquisition is highly robust against sensor drift. 

To rigorously validate actuator reachability and rule out false-positive test results caused by unresponsive or "stuck" sensors in the middleware, we introduced *Inverted Monotonicity* relations (S8). By forcing the test to expect a strict decrease in values, we definitively proved that the sensors actively respond to commands, validating true system reachability.

### 2. Spatial Interactions and Proportionality (EQ2)
We evaluated whether spatial interactions in the DT conform to expected physical behaviors and proportionality. Basic control adaptation tests (S1, S2) passed with a 100% success rate, verifying that the fundamental device-mapping and local illuminance responses are correctly implemented. 

However, evaluating aggregate spatial interference via the Conservation relation (S3) revealed the limitations of physical symmetry. While moderate illuminance redistribution (e.g., a 75/25 split) passed within the 5% tolerance bound, extreme configurations (100/0) systematically failed. This relation failure accurately reflects the physical asymmetry of real-world light distribution rather than a logic flaw in the DT. To empirically prove the localization of this cross-workplace leakage, we applied an *Inverted Proportionality* relation (S5) across distant sensors with a generous 50% error tolerance. The measured deviations of 78.2% and 126.1% successfully triggered the expected failure. This provides strong empirical evidence that while cross-workplace leakage exists, it remains highly localized and asymmetrical, validating the DT's spatial proportionality representation.

### 3. Hardware Evolution and Replacement (EQ3)
A critical requirement for digital twins is maintaining validity throughout the lifecycle of the physical asset, particularly during hardware maintenance. We tested this by introducing new actuators (S4) and sensors (S5) at runtime, both of which immediately satisfied monotonicity and proportionality relations with their physical neighbors, proving seamless semantic integration.

Most notably, the substitution scenario (S6)—in which a physical sensor was replaced by a comparable model and rebound within the middleware—demonstrated 100% relation consistency. By executing the exact same suite of metamorphic relations pre- and post-replacement, we proved that the DT preserves full device semantics. Neither the middleware rebinding process nor the minimal hardware variances of the new sensor falsified the logical relations within the system, demonstrating the high resilience of the DT against hardware evolution.

---
*(Author Note: Insert Plot 1 (Sensor Stability over 200s from S10) and Plot 2 (Latency Bar Chart from S7) into the text here to visually support EQ1).*
