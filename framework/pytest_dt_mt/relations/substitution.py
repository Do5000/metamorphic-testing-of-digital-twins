import pytest
import os
import json

def _load_json_profile(file_path):
    """Internal helper to load reference tables with robust path resolution."""
    if os.path.exists(file_path):
        full_path = file_path
    else:
        # Resolve framework folder relative to this file:
        # __file__ is plugin_dir/relations/substitution.py
        # parent of substitution.py is relations/
        # parent of relations/ is pytest_dt_mt/
        # parent of pytest_dt_mt/ is framework/
        plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        framework_dir = os.path.dirname(plugin_dir)
        full_path = os.path.join(framework_dir, file_path)

    if not os.path.exists(full_path):
        return None
    try:
        with open(full_path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def validate(result, **kwargs):
    __tracebackhide__ = True
    new_val, neighbor_val = float(result[0]), float(result[1])
    tolerance = kwargs.get("tolerance", 0.0)
    profile_path = kwargs.get("profile", "sensor_profile.json")
    profile_data = _load_json_profile(profile_path)
    
    if profile_data is None:
        pytest.fail(f"Metamorphic Relation (Substitution) failed: Reference profile '{profile_path}' not found or invalid.", pytrace=False)
        
    # Handle dictionary structure vs old flat list structure
    if isinstance(profile_data, dict):
        profile = profile_data.get("profile", [])
    else:
        profile = profile_data
        
    # Find best match in table based on neighbor sensor
    try:
        best_match = min(profile, key=lambda x: abs(x["neighbor_sensor"] - neighbor_val))
        historic_old_val = best_match["old_sensor"]
        match_ref_val = best_match["neighbor_sensor"]
    except (KeyError, TypeError):
        pytest.fail(f"Metamorphic Relation (Substitution) failed: Profile format invalid (missing 'neighbor_sensor' or 'old_sensor').", pytrace=False)

    diff = abs(new_val - historic_old_val)
    max_val = max(abs(historic_old_val), abs(new_val), 1.0)
    allowed = tolerance if tolerance > 1.0 else max_val * tolerance
    
    if diff > allowed:
        pytest.fail(f"Metamorphic Relation (Substitution) failed: New sensor {new_val} vs Historical old sensor {historic_old_val} (Matched by neighbor {neighbor_val} approx {match_ref_val} | diff {diff} > allowed {allowed})", pytrace=False)
    
    print(f"\n      [MR CHECK] Substitution PASSED: New sensor {new_val} matches Historical entry {historic_old_val} (Neighbor match: {neighbor_val} approx {match_ref_val})")
