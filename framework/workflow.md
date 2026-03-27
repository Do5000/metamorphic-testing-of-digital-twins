## Workflow

    1) connect VPN and login to Firewall
    2) python translation_unit_mockbackend_middleware.py
    3) see all connected devices http://localhost:8083/api/2/search/things

    4) possible commands:
        python set_light_ditto.py light.norden_fenster on
        python set_light_ditto.py light.norden_fenster off
        python set_light_ditto.py light.sueden_fenster on
        python set_light_ditto.py light.sueden_fenster off

        python set_switch_ditto.py switch.licht_schalter on
        python set_switch_ditto.py switch.licht_schalter off

        python set_cover_ditto.py cover.cover_norden 50 
        python set_cover_ditto.py cover.cover_norden 100
        python set_cover_ditto.py cover.cover_sueden 50 
        python set_cover_ditto.py cover.cover_sueden 100
