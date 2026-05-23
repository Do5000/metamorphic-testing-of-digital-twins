import pytest
import os
import json
from pytest_dt_mt.relations import substitution

@pytest.fixture
def temp_profile_json(tmp_path):
    """Fixture to generate temporary profile JSON files in different formats."""
    flat_list = [
        {"brightness_cmd": 0, "old_sensor": 10.0, "neighbor_sensor": 15.0},
        {"brightness_cmd": 50, "old_sensor": 50.0, "neighbor_sensor": 55.0},
        {"brightness_cmd": 100, "old_sensor": 100.0, "neighbor_sensor": 105.0}
    ]
    
    dict_format = {
        "light_id": "light.schreibtisch_lampe",
        "sensor_old_id": "sensor.esp_c3_helligkeit",
        "sensor_neighbor_id": "sensor.esp_c6_helligkeit",
        "profile": flat_list
    }
    
    flat_file = tmp_path / "sensor_profile_flat.json"
    with open(flat_file, "w") as f:
        json.dump(flat_list, f, indent=4)
        
    dict_file = tmp_path / "sensor_profile_dict.json"
    with open(dict_file, "w") as f:
        json.dump(dict_format, f, indent=4)
        
    return str(flat_file), str(dict_file)

def test_substitution_validation_with_flat_format(temp_profile_json):
    flat_path, _ = temp_profile_json
    
    # Test matching scenario: val_new=50.5 (should match 50.0 historical old sensor), val_neighbor=54.8 (matches 55.0 neighbor sensor)
    # result = (val_new, val_neighbor)
    # tolerance = 0.1 (10% of max(50.0, 50.5, 1.0) = 5.05 allowed)
    # diff = abs(50.5 - 50.0) = 0.5 <= 5.05 -> should pass!
    result = (50.5, 54.8)
    substitution.validate(result, profile=flat_path, tolerance=0.1)
    
    # Test failing scenario: val_new=60.0 (historical old is 50.0), val_neighbor=54.8
    # diff = abs(60.0 - 50.0) = 10.0 > 6.0 allowed -> should fail!
    with pytest.raises(pytest.fail.Exception) as exc_info:
        substitution.validate((60.0, 54.8), profile=flat_path, tolerance=0.1)
    assert "Metamorphic Relation (Substitution) failed" in str(exc_info.value)

def test_substitution_validation_with_dict_format(temp_profile_json):
    _, dict_path = temp_profile_json
    
    # Test matching scenario using new dictionary structure: should extract the list and pass!
    result = (50.5, 54.8)
    substitution.validate(result, profile=dict_path, tolerance=0.1)
    
    # Test failing scenario: should extract list and fail correctly!
    with pytest.raises(pytest.fail.Exception) as exc_info:
        substitution.validate((60.0, 54.8), profile=dict_path, tolerance=0.1)
    assert "Metamorphic Relation (Substitution) failed" in str(exc_info.value)
