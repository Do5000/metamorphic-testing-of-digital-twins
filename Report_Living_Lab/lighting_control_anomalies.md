# Lighting Control Anomalies in the Living Lab 


---

## 1. Category 1: Automatic Shutoff After ~10s (16 Tests)

### Behavior
Luminaires actuate as commanded, remain illuminated for approximately **9 to 10 seconds** (aprox 35 to 40 seconds after the first command)

### Root Cause
An overruling from the buildings control?

### Affected Tests (16)

| Log File | Test Case | Actuation Command | Live Monitor Progression |
| :--- | :--- | :--- | :--- |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_TSL2_Keyboard_spec-1-5` | All 4 luminaires = 100% | ON at 14s ($4,002\text{ lx}$) $\rightarrow$ spontaneously OFF at 24s ($1,382\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_sueden_fenster-1-5` | `sueden_fenster` = 100% | ON at 13s ($249\text{ lx}$) $\rightarrow$ spontaneously OFF at 23s ($177\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_TSL3_UpperScreen_spec-2-5` | All 4 luminaires = 100% | ON at 9s ($3,412\text{ lx}$) $\rightarrow$ spontaneously OFF at 19s ($1,822\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_norden_tuer-2-5` | `norden_tuer` = 100% | ON at 12s ($207\text{ lx}$) $\rightarrow$ spontaneously OFF at 22s ($183\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_TSL1_LowerScreen_spec-4-5` | All 4 luminaires = 100% | ON at 6s ($1,781\text{ lx}$) $\rightarrow$ spontaneously OFF at 16s ($507\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_sueden_tuer-4-5` | `sueden_tuer` = 100% | ON at 5s ($110\text{ lx}$), held until query dropped to baseline ($82\text{ lx}$) |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_sueden_fenster-5-5` | `sueden_fenster` = 100% | ON at 8s ($231\text{ lx}$) $\rightarrow$ spontaneously OFF at 19s ($165\text{ lx}$) |
| `s1_living_lab_monotony_night_fail.log` | `TC_S1_Monotony_norden_fenster-1-5` | `norden_fenster` = 100% | ON at 4s ($65\text{ lx}$) $\rightarrow$ spontaneously OFF at 13s ($0.83\text{ lx}$) |
| `s1_living_lab_monotony_night_fail.log` | `TC_S1_Monotony_norden_fenster-2-5` | `norden_fenster` = 100% | ON at 12s ($63\text{ lx}$) $\rightarrow$ spontaneously OFF at 22s ($0.83\text{ lx}$) |
| `s1_living_lab_monotony_night_fail.log` | `TC_S1_Monotony_norden_fenster-3-5` | `norden_fenster` = 100% | ON at 9s ($63\text{ lx}$) $\rightarrow$ spontaneously OFF at 19s ($0.83\text{ lx}$) |
| `s2_living_lab_invariance_ceiling_fail.log` | `TC_S2_Invariance-2-5` | All 4 luminaires = 75% | ON at 12s ($142\text{ lx}$) $\rightarrow$ spontaneously OFF at 22s ($0.83\text{ lx}$) |
| `s2_living_lab_invariance_ceiling_fail.log` | `TC_S2_Invariance-4-5` | All 4 luminaires = 75% | ON at 11s ($160\text{ lx}$) $\rightarrow$ spontaneously OFF at 21s ($0.83\text{ lx}$) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_100-1-5` | `sueden_tuer` = 100% | ON at 8s ($24\text{ lx}$) $\rightarrow$ spontaneously OFF at 18s ($0.83\text{ lx}$) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_100-2-5` | `sueden_tuer` = 100% | ON at 0s ($29\text{ lx}$) $\rightarrow$ spontaneously OFF at 17s ($0.83\text{ lx}$) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_100-3-5` | `sueden_tuer` = 100% | ON at 0s ($30\text{ lx}$) $\rightarrow$ spontaneously OFF at 16s ($0.83\text{ lx}$) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_100-4-5` | `sueden_tuer` = 100% | ON at 0s ($30\text{ lx}$) $\rightarrow$ spontaneously OFF at 15s ($0.83\text{ lx}$) |

---

## 2. Category 2: Zero Response to Actuation Command (6 Tests)

### Behavior
The luminaires exhibit zero physical response to turn-on commands. The sensor remains completely flatlined at the pre-actuation baseline across all 24 seconds of monitoring.

### Affected Tests (6)

| Log File | Test Case | Actuation Command | Live Monitor Progression |
| :--- | :--- | :--- | :--- |
| `s1_living_lab_monotony_daylight_fail.log` | `TC_S1_Monotony_TSL2_Keyboard_spec-5-5` | All 4 luminaires = 100% | 24s flatline at $253–254\text{ lx}$ (no response to command) |
| `s1_living_lab_monotony_night_fail.log` | `TC_S1_Monotony_norden_tuer-5-5` | `norden_tuer` = 100% | 24s flatline at $0.83\text{ lx}$ (no response to command) |
| `s2_living_lab_invariance_ceiling_fail.log` | `TC_S2_Invariance-1-5` | All 4 luminaires = 75% | Phase 3: 24s flatline at $0.83\text{ lx}$ |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_75-3-5` | `norden_tuer` = 75%, `sueden_tuer` = 25% | Phase 1: 24s flatline at $0.83\text{ lx}$ (Phase 2 actuated normally) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_75-4-5` | `norden_tuer` = 75%, `sueden_tuer` = 25% | Phase 1: 24s flatline at $0.83\text{ lx}$ (Phase 2 actuated normally) |
| `s3_living_lab_conservation_fail.log` | `TC_S3_Conservation_75-5-5` | `norden_tuer` = 75%, `sueden_tuer` = 25% | Phase 1: 24s flatline at $0.83\text{ lx}$ (Phase 2 actuated normally) |

---

