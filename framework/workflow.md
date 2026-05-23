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

### Workflow Testing
    pytest mr/mt_light_invariance_test.py -v -s --wait-time=5.0 --monitor 
    pytest mr/mt_light_monotony_test.py -v -s --wait-time=5.0 --monitor 
    pytest mr/mt_light_conservation_test.py -v -s --wait-time=5.0 --monitor 

    pytest mr/ -v -s --wait-time=5.0 --monitor     (all tests)

    pytest tests/test_home_lab.py -v -s --wait-time=5.0 --monitor 
    pytest tests/test_living_lab.py -v -s --wait-time=5.0 --monitor 

    


## Workflow Raspi Lab

    1) python3 ./translationunit_mockbackend_raspi.py
    2) python3 ./discover_catalog.py
    3) see all connected devices in device_catalog.json or http://localhost:8083/api/2/search/things

## Workflow Substitution Relation

    1) 

    
