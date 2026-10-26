# Metamorphic Testing DSL Documentation

The **Metamorphic Testing Domain-Specific Language** is designed for defining, standardizing, and automatically executing metamorphic tests on Digital Twins and IoT systems (e.g., Smart Home / Living Lab environments).

Files written in this language use the extension **`.mt`**. They are validated using a Langium-based language server, compiled into machine-readable JSON test definitions, and subsequently executed by a pytest-based metamorphic test runner.

---

## Table of Contents
1. [Basic Structure of a `.mt` File](#1-basic-structure-of-a-mt-file)
2. [Lifecycle Hooks and Statements](#2-lifecycle-hooks-and-statements)
   - [2.1. Setting State (`set`)](#21-setting-state-set)
   - [2.2. Checking Preconditions (`precondition`)](#22-checking-preconditions-precondition)
   - [2.3. Latency and Settling Time Calibration (`calibrateLatency`)](#23-latency-and-settling-time-calibration-calibratelatency)
3. [Test Definitions (`test`)](#3-test-definitions-test)
   - [3.1. Structure and Test Parameters](#31-structure-and-test-parameters)
   - [3.2. The 5 Core Relations](#32-the-5-core-relations)
     - [1. Monotonicity](#1-monotonicity-monotonicity)
     - [2. Invariance](#2-invariance-invariance)
     - [3. Conservation](#3-conservation-conservation)
     - [4. Stability](#4-stability-stability)
     - [5. Proportionality](#5-proportionality-proportionality)
   - [3.3. Inverted Relations (`not`)](#33-inverted-relations-not)
4. [Live Validation & Device Catalog Integration (LSP)](#4-live-validation--device-catalog-integration-lsp)
5. [Test Execution and Pytest Runner](#5-test-execution-and-pytest-runner)
   - [5.1. Selective Automatic Compilation (`-k`)](#51-selective-automatic-compilation--k)
   - [5.2. CLI Flags & Monitoring](#52-cli-flags--monitoring)
6. [Central Default Values (Single Point of Truth)](#6-central-default-values-single-point-of-truth)
7. [CLI and DSL Developer Commands](#7-cli-and-dsl-developer-commands)

---

## 1. Basic Structure of a `.mt` File

A `.mt` file is typically structured into two main parts:
1. **Lifecycle Hooks**: Set up preconditions, reset devices before or after test executions, and perform automated latency calibration.
2. **Test Definitions (`test`)**: Declare metamorphic relations to be evaluated along with actuators, sensors, and test values.

```mt
beforeAll {
    // One-time setup of test environment & calibration
}

beforeEach {
    // Reset or defined initial state before each test
}

test "TC_Example_Test" {
    // Test configuration
}

afterAll {
    // Teardown / restoration after all tests finish
}
```

---

## 2. Lifecycle Hooks and Statements

The DSL provides three lifecycle hooks:
- `beforeAll`: Executed **once before all tests** in the file.
- `afterAll`: Executed **once after all tests** in the file.
- `beforeEach`: Executed **before each individual test case**.

Within these blocks, the following statements can be used:

### 2.1. Setting State (`set`)
Actuates devices or sets properties (features) directly in the Digital Twin.
- **Syntax:** `set "DEVICE" feature "FEATURE" to VALUE`
- **Examples:**
  ```mt
  set "light.desk_lamp" feature "state" to "off"
  set "light.desk_lamp" feature "brightness" to 50
  set "automation.living_room_on" feature "state" to "off"
  ```

### 2.2. Checking Preconditions (`precondition`)
Evaluates an environment or state reading before executing tests. If the precondition is not met, the test run is skipped without producing false failures.
- **Syntax:** `precondition "SENSOR" feature "FEATURE" equals VALUE [skipMessage "REASON"]`
- **Example:**
  ```mt
  precondition "sun.sun" feature "state" equals "below_horizon" skipMessage "This scenario must be tested at night."
  ```

### 2.3. Latency and Settling Time Calibration (`calibrateLatency`)
Automatically measures the physical response and settling time (pipeline latency) between an actuator command and the corresponding sensor response. The measured value is dynamically applied as the wait duration (`wait_dt`) for subsequent tests.

```mt
calibrateLatency {
    actuator "light.desk_lamp" feature "brightness"
    sensor "sensor.esp_c6_brightness" feature "state"
    valOff "0"
    valOn "100"
    
    // Optional parameters for fine-tuning:
    minChangePercent 0.01      // Minimum change threshold (1%) to detect a response
    maxSettleTolerance 0.01    // Allowed fluctuation band for steady state (1%)
    settleTime 5.0             // Settling time window in seconds
    toleranceFactor 1.2        // Multiplicative safety factor (+20%)
    addSeconds 1               // Additive buffer in seconds (+1s)
    timeout 30.0               // Maximum timeout per calibration run
    runs 1                     // Number of measurement runs (for averaging)
}
```

#### Parameter Reference for `calibrateLatency`:
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `actuator` | String | Actuator device ID (*Required*) |
| `actuatorFeature` | String | Feature to manipulate (e.g., `"brightness"`, default: `"state"`) |
| `sensor` | String | Sensor device ID (*Required*) |
| `sensorFeature` | String | Observed sensor feature (default: `"state"`) |
| `valOff` | Value | Baseline / off value (*Required*) |
| `valOn` | Value | Actuation value for latency measurement (*Required*) |
| `minChangePercent` | Number | Threshold for detecting the initial measurable sensor response |
| `maxSettleTolerance`| Number | Fluctuation tolerance band for the settled reading |
| `settleTime` | Number | Duration the reading must remain stable |
| `toleranceFactor` | Number | Multiplicative safety factor applied to the measured latency (e.g., 1.2 = +20%) |
| `addSeconds` | Number | Fixed additive time buffer on top of the calculated wait time |
| `timeout` | Number | Maximum wait time before the measurement times out |
| `runs` | Number | Number of measurement runs for aggregation |

---

## 3. Test Definitions (`test`)

A test block defines a metamorphic relationship between input actions and output sensor observations.

### 3.1. Structure and Test Parameters

```mt
test "Test_Name" {
    relation: <Relation> [tolerance: <Number>] [duration: <Number>] [waitTime: <Number>]
    
    actuators [ "DEVICE" feature "FEATURE", ... ]
    sensors [ "SENSOR" feature "FEATURE", ... ]
    
    sourceAction [ VALUE, ... ]
    intermediateAction [ VALUE, ... ]    // Optional (e.g. for invariance reset)
    followUpAction [ VALUE, ... ]
}
```

#### Available Parameters:
- **`actuators [...]`**: List of target actuators. Relations like `conservation` or `proportionality` support multiple actuators.
- **`sensors [...]`**: List of sensors to observe.
- **`sourceAction [...]`**: Source input values for the actuators. The number of values must match the number of defined `actuators`.
- **`intermediateAction [...]`**: Intermediate state (essential for invariance reset checks).
- **`followUpAction [...]`**: Follow-up input values for the metamorphic relation.
- **`tolerance: <Number>`**: Allowed tolerance $\tau$. When $\tau \le 1.0$, it is treated as a relative tolerance (e.g., `0.05` = 5%), otherwise as an absolute tolerance.
- **`duration: <Number>`**: Observation duration in seconds (specifically for `stability`).
- **`waitTime: <Number>`**: Optional manual override for the physical settling wait time of this test.

---

### 3.2. The 5 Core Relations

#### 1. Monotonicity (`monotonicity`)
- **Example:**
  ```mt
  test "TC_S1_Monotony_80" {
      relation: monotonicity tolerance: 0.02
      actuators [ "light.desk_lamp" feature "brightness" ]
      sensors [ "sensor.esp_c6_brightness" feature "state" ]
      sourceAction [ "20" ]
      followUpAction [ "80" ]
  }
  ```

#### 2. Invariance (`invariance`)
- **Example:**
  ```mt
  test "TC_S2_Invariance" {
      relation: invariance tolerance: 0.05
      actuators [ "light.desk_lamp" feature "brightness" ]
      sensors [ "sensor.esp_c6_brightness" feature "state" ]
      sourceAction [ "100" ]
      intermediateAction [ "0" ]
      followUpAction [ "100" ]
  }
  ```

#### 3. Conservation (`conservation`)
- **Example:**
  ```mt
  test "TC_S3_Conservation_75" {
      relation: conservation tolerance: 0.05
      actuators [ 
          "light.desk_lamp" feature "brightness", 
          "light.vintage_lamp" feature "brightness" 
      ]
      sensors [ "sensor.esp_c6_brightness" feature "state" ]
      sourceAction [ "75", "25" ]
      followUpAction [ "25", "75" ]
  }
  ```

#### 4. Stability (`stability`)
- **Example:**
  ```mt
  test "TC_S10_Stability_esp_c6" {
      relation: stability tolerance: 0.05 duration: 60.0
      actuators [ "light.desk_lamp" feature "brightness" ]
      sensors [ "sensor.esp_c6_brightness" feature "state" ]
      sourceAction [ "50" ]
  }
  ```

#### 5. Proportionality (`proportionality`)
- **Example:**
  ```mt
  test "TC_S5_Proportionality_Synchronous_Scaling" {
      relation: proportionality tolerance: 0.05
      actuators [ 
          "light.desk_lamp" feature "brightness", 
          "light.vintage_lamp" feature "brightness" 
      ]
      sensors [ 
          "sensor.esp_c6_brightness" feature "state", 
          "sensor.esp_c3_brightness" feature "state" 
      ]
      sourceAction [ "20", "20" ]
      followUpAction [ "80", "80" ]
  }
  ```

---

### 3.3. Inverted Relations (`not`)

Any relation can be inverted by prefixing the relation identifier with the keyword `not`:
```mt
test "TC_Monotony_Fault_Check" {
    relation: not monotonicity tolerance: 0.02
    actuators [ "light.desk_lamp" feature "brightness" ]
    sensors [ "sensor.esp_c6_brightness" feature "state" ]
    sourceAction [ "100" ]
    followUpAction [ "0" ]
}
```
- **Semantics:** The test passes if and only if the original relation is **violated**.
- **Use Cases:** Fault injection verification, negative testing, and detecting frozen sensor states.

---

## 4. Live Validation & Device Catalog Integration (LSP)

The MT-DSL Language Server validates `.mt` files in real time in the editor and during CLI generation:

1. **Comparison with `device_catalog.json`:**
   - Validates that referenced devices exist.
   - Validates that the specified `feature` is defined on that device in the Digital Twin catalog.
2. **Fuzzy Typo Suggestions (Levenshtein Distance):**
   - If an unrecognized device ID is typed (e.g., `"light.desk"`), the validator provides an interactive warning:
     *`Device "light.desk" not found. Did you mean "light.desk_lamp"?`*
3. **Cardinality Verification:**
   - Ensures that the number of values in `sourceAction`, `intermediateAction`, and `followUpAction` strictly matches the number of defined `actuators`.
4. **Runtime Null Guard:**
   - If a sensor returns `None` during test execution (e.g., due to an offline physical device or communication timeout), the test immediately fails with a descriptive `AssertionError` to prevent misleading calculations.

---

## 5. Test Execution and Pytest Runner

Tests are executed using the central runner [`tests/test_dsl_runner.py`](../tests/test_dsl_runner.py).

### 5.1. Selective Automatic Compilation (`-k`)

When invoking `pytest` with a `-k` filter, the runner automatically compiles **only the `.mt` files that match the filter keyword** into JSON before collecting tests:

```bash
# Run only Home Lab scenarios:
pytest tests/test_dsl_runner.py -k "my_home_lab" -v --capture=tee-sys

# Run only Living Lab scenarios:
pytest tests/test_dsl_runner.py -k "living_lab" -v --capture=tee-sys

# Run a specific scenario (e.g., S3 Conservation):
pytest tests/test_dsl_runner.py -k "s3_conservation" -v --capture=tee-sys
```

### 5.2. CLI Flags & Monitoring

| Flag | Function |
| :--- | :--- |
| `-v` | Verbose output displaying detailed test outcomes |
| `--wait-time=X` | Overrides the global default wait time (in seconds) |
| `--capture=tee-sys` | Displays terminal output live **and** stores it for test reports |
| `--monitor` | Enables live sensor data streaming during test execution |
| `--log` | Generates a structured session log file in the `test_reports/` directory |
| `--count=N` | Repeats test suite execution $N$ times (for stress testing & detecting flaky tests) |
| `--repeat-scope=session` | Runs the entire test suite from start to finish before starting the next repetition |

**Recommended Standard Invocation:**
```bash
pytest tests/test_dsl_runner.py -k "s1_monotony" -v --wait-time=5.0 --capture=tee-sys --monitor --log
```

---

## 6. Central Default Values (Single Point of Truth)

All default parameters of the framework are centrally managed in [`pytest_dt_mt/config.py`](../pytest_dt_mt/config.py):

```python
DEFAULT_MIN_CHANGE_PERCENT = 0.01      # 1% minimum change threshold for latency detection
DEFAULT_MAX_SETTLE_TOLERANCE = 0.01    # 1% fluctuation tolerance for steady state
DEFAULT_SETTLE_TIME = 5.0             # 5 seconds settling window
DEFAULT_TOLERANCE_FACTOR = 1.2        # 20% margin on measured response time
DEFAULT_ADD_SECONDS = 1.0             # 1 second additive buffer
DEFAULT_TIMEOUT = 5.0                 # Timeout for calibration runs
DEFAULT_CALIBRATION_RUNS = 1          # 1 calibration run
DEFAULT_MONITOR_INTERVAL = 0.5        # 500ms sampling rate for live monitoring
DEFAULT_RELATION_TOLERANCE = 0.05     # 5% default relation tolerance
DEFAULT_STABILITY_DURATION = 10.0     # 10 seconds default stability observation duration
DEFAULT_GLOBAL_WAIT_TIME = 30.0       # Global fallback wait time
```

---

## 7. CLI and DSL Developer Commands

Within the `framework/dsl/` directory:

```bash
# 1. Compile all .mt files into JSON test definitions:
npm run generate

# 2. Compile a specific .mt file manually:
node out/cli/main.js generate scenarios/my_home_lab/s1_monotony.mt -d generated/

# 3. Regenerate the Langium parser and AST (after editing mt-dsl.langium):
npm run langium:generate

# 4. Compile TypeScript files and bundles:
npm run build

# 5. Continuous watch mode for active development:
npm run watch
```

### VS Code Extension Development Host:
1. Open `framework/dsl` in VS Code.
2. Run `npm install`.
3. Press **F5**: A new VS Code window launches with live MT-DSL language support (syntax highlighting, autocompletion, diagnostics).
