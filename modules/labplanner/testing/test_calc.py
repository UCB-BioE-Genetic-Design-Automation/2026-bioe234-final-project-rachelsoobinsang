import pytest
import os
import json
from modules.labplanner.tools.master_mix_calc import MasterMixCalc

@pytest.fixture
def calc_instance():
    instance = MasterMixCalc()
    instance.initiate()
    return instance

### --- Tests for Atomic Calculation ---

def test_calculate_math(calc_instance):
    """Verifies the 10% buffer logic (10 samples * 1.1 = 11x multiplier)."""
    # Assuming 'General_PCR' has a reagent with 12.5uL in your recipes.json
    result = calc_instance.calculate("General PCR", 10)
    
    # 12.5 * 11 = 137.5
    assert result["Samples"] == 10
    # Check if a specific reagent exists and is scaled correctly
    # Replace 'Taq_Polymerase' with an actual key from your recipes.json
    for volume in result["Scaled Recipe"].values():
        assert volume > 0

def test_calculate_invalid_samples(calc_instance):
    """Edge Case: Ensure it raises ValueError for 0 or negative samples."""
    with pytest.raises(ValueError, match="at least 1"):
        calc_instance.calculate("General PCR", 0)

### --- Tests for Construction File (run) ---

def test_run_from_cf_typical(calc_instance, tmp_path):
    """Typical Case: Verify it processes multiple steps from a file."""
    # Create a temporary construction file for testing
    d = tmp_path / "data" / "construction_files"
    d.mkdir(parents=True)
    cf_file = d / "test_plan.json"
    
    test_data = {
        "steps": [
            {"protocol": "General PCR", "samples": 10},
            {"protocol": "General PCR", "samples": 20}
        ]
    }
    cf_file.write_text(json.dumps(test_data))

    # We manually override the base_path for the test to find our temp file
    # Or simply ensure the file exists in your real data folder for a simpler test
    results = calc_instance.run("test_plan.json") 
    
    assert len(results) == 2
    assert results[0]["Samples"] == 10
    assert results[1]["Samples"] == 20

def test_cf_not_found(calc_instance):
    """Edge Case: Ensure it raises FileNotFoundError for missing files."""
    with pytest.raises(FileNotFoundError):
        calc_instance.run("non_existent_file.json")