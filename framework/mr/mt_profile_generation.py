import pytest
import json
import os
import asyncio

async def beforeAll(dt_adapter):
    print("\n[HOOK] beforeAll: Preparing environment for profile generation")
    # All lights off, automations off
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "off")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")

@pytest.mark.asyncio
async def test_generate_sensor_profile(dt_adapter, wait_dt):
    """
    Generates a reference profile for sensor substitution.
    Records values for the 'old' sensor and the 'neighbor' sensor across different brightness levels.
    """
    profile = []
    light_id = "light.schreibtisch_lampe"
    sensor_old_id = "sensor.arbeitsplatz_helligkeit"
    sensor_neighbor_id = "sensor.arbeitsplatz_helligkeit_2"
    
    # Step through brightness levels (0 to 255)
    # We use smaller steps for a "lückenlose" table as requested
    brightness_levels = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    
    for b in brightness_levels:
        print(f"\n[STEP] Testing brightness level: {b}")
        if b == 0:
            await dt_adapter.set_feature_value(light_id, "state", "off")
        else:
            # await dt_adapter.set_feature_value(light_id, "state", "on")
            await dt_adapter.set_feature_value(light_id, "brightness", b)
        
        # Wait for physical stabilization and DT update
        await wait_dt()
        
        # Read current values
        val_old = await dt_adapter.get_feature_value(sensor_old_id, "state")
        val_neighbor = await dt_adapter.get_feature_value(sensor_neighbor_id, "state")
        
        profile.append({
            "brightness_cmd": b,
            "old_sensor": val_old,
            "neighbor_sensor": val_neighbor
        })
        print(f"       Recorded -> Old: {val_old}, Neighbor: {val_neighbor}")

    # Save the profile to a JSON file
    output_file = "sensor_profile.json"
    with open(output_file, "w") as f:
        json.dump(profile, f, indent=4)
    
    print(f"\n[SUCCESS] Profile saved to {output_file}")

async def afterAll(dt_adapter):
    print("\n[HOOK] afterAll: Restoring environment")
    await dt_adapter.set_feature_value("light.schreibtisch_lampe", "state", "off")
    await dt_adapter.set_feature_value("automation.wohnzimmer_ein", "state", "on")
    await dt_adapter.set_feature_value("automation.wohnzimmer_aus", "state", "on")
