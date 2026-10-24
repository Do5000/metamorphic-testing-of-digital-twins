## Workflow Living Lab

Always: source venv/bin/activate in /framework!!!!

    1) connect VPN and login to Firewall
    2) python3 ./discover_catalog.py
    3) see all connected devices in device_catalog.json or http://{IP}:8083/api/2/search/things

## Workflow Raspi Lab

    1) python3 ./translationunit_mockbackend_raspi.py
    2) python3 ./discover_catalog.py
    3) see all connected devices in device_catalog.json or http://localhost:8083/api/2/search/things

## Flags

    -k: select specific tests
    -v: clean output (always required)
    --capture=no: Turns off all capturing. You see everything live, but no output is saved for test reports
    --capture=sys: Captures and saves all printed text, but you see nothing on your screen while tests run
    --capture=tee-sys: Does both. Your print statements display live on your screen, and they are saved internally for test reports or plugins

    --monitor: Prints LiveValues from the Sensors
    --log: Creates a logfile
    --wait-time=x: default wait-time
    --count=x: Defines how many times the tests should be executed (e.g. --count=2 runs them twice). Useful for stress testing or finding flaky tests.
    --repeat-scope=session: Modifies the repetition order. Instead of repeating each test immediately (Test A -> Test A -> Test B -> Test B), it ensures the entire test suite is completed first before starting the next loop (Test A -> Test B -> Test A -> Test B), simulating a much more realistic execution flow.

### Example Options:
#### Everything:
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0 --capture=tee-sys --monitor --log

#### Without Logfile:
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0 --capture=tee-sys --monitor 

#### Without LiveValues
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0 --capture=tee-sys --log

#### Minimal Output with log (attention: without --capture=tee-sys --capture=sys --log can't save anything)
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0 --capture=sys --log

#### Minimal Output (attention: without --capture=tee-sys or --capture=sys --log can't save anything)
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0 

#### Only Terminal Output (attention: without --capture=tee-sys or --capture=sys --log can't save anything ; with --log: only PASSED/FAILED Result is saved in a logfile)
    pytest tests/test_dsl_runner.py -k "test_home_lab"  -v --wait-time=6.0  --capture=no

-k "test_home_lab" executes every test file with "test_home_lab" in the name, that is in the generated directory (attention: if you remove the .mt file from the scenarios, it doesn't automatically be removed from the generated json files)

    
