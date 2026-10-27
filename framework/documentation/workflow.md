# Test Execution & Operation Workflow

Ensure the virtual environment is activated before running tests locally:
```bash
source venv/bin/activate
```
Or use Docker directly without any manual virtual environment setup:
```bash
cd framework
docker compose run --rm framework pytest tests/test_dsl_runner.py -v --capture=tee-sys
```

---

## 1. Environment Setup Workflows

### Living Lab Workflow
1. Connect to the network (e.g., via VPN / Firewall).
2. Query and synchronize the device catalog:
   ```bash
   python3 ./discover_catalog.py
   ```
3. Inspect connected devices in `device_catalog.json` or query the Ditto Search API directly:
   ```
   http://{DITTO_IP}:8083/api/2/search/things
   ```

### Raspberry Pi / Local Lab Workflow
1. Start the backend adapter
   ```bash
   python3 ./translationunit_mockbackend_raspi.py
   ```
2. Query and synchronize the device catalog:
   ```bash
   python3 ./discover_catalog.py
   ```
3. Verify device status in `device_catalog.json` or via HTTP:
   ```
   http://localhost:8083/api/2/search/things
   ```

---

## 2. Pytest Execution Flags

| Flag | Description |
| :--- | :--- |
| `-k <filter>` | Selects and executes specific tests matching the keyword (e.g. `-k "my_home_lab"`, `-k "living_lab"`). |
| `-v` | Verbose output displaying test names and execution details. |
| `--wait-time=<sec>` | Overrides the default post-actuation waiting time for settling. |
| `--monitor` | Prints live sensor values continuously during settling time. |
| `--log` | Generates a structured session log file in the `test_reports/` directory. |
| `--count=<N>` | Runs the test suite $N$ times (for stress testing and detecting flaky tests). |
| `--repeat-scope=session` | Completes the entire test suite before starting the next repetition cycle. |
| `--capture=tee-sys` | Recommended. Displays printed statements live in the console **and** preserves them for test reports and loggers. |
| `--capture=sys` | Captures output silently without console display; saved to test reports. |
| `--capture=no` | Direct console passthrough without capturing into test report structures. |

---

## 3. Execution Examples

### Comprehensive Run (Live Monitoring + Session Log):
```bash
pytest tests/test_dsl_runner.py -k "my_home_lab" -v --wait-time=6.0 --capture=tee-sys --monitor --log
```

### Run with Live Monitoring (Without Logfile):
```bash
pytest tests/test_dsl_runner.py -k "my_home_lab" -v --wait-time=6.0 --capture=tee-sys --monitor
```

### Run with Session Log (Without Live Monitoring):
```bash
pytest tests/test_dsl_runner.py -k "my_home_lab" -v --wait-time=6.0 --capture=tee-sys --log
```

### Minimal Console Output:
```bash
pytest tests/test_dsl_runner.py -k "my_home_lab" -v --wait-time=6.0
```

> **Note on `-k` filtering:**
> The `-k` option matches against scenario file and test names. The test runner will automatically compile only the corresponding `.mt` scenarios into `dsl/generated/` prior to test execution.
