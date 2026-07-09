## Workflow Living Lab

Always: source venv/bin/activate in /framework!!!!

    1) connect VPN and login to Firewall
    2) python3 ./translationunit_mockbackend_middleware.py
    Optional:  python3 ./pipline_latenz/check_pipeline.py   
    3) python3 ./discover_catalog.py
    4) see all connected devices in device_catalog.json or http://localhost:8083/api/2/search/things

    5) possible commands:
        python set_light_ditto.py light.norden_fenster on
        python set_light_ditto.py light.norden_fenster off (only state)
        python set_light_ditto.py light.sueden_fenster 0 (brightness)
        python set_light_ditto.py light.sueden_fenster 50 (brightness)

        python set_switch_ditto.py switch.licht_schalter on
        python set_switch_ditto.py switch.licht_schalter off

        python set_cover_ditto.py cover.cover_norden 50 
        python set_cover_ditto.py cover.cover_norden 100 (only position)
        python set_cover_ditto.py cover.cover_sueden 50 30 (Position and Tilt)
        python set_cover_ditto.py cover.cover_sueden 100 40

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

    
