import pytest
import os
from modules.labplanner.tools.master_mix_calc import MasterMixCalc

@pytest.fixture
def calc():
    c = MasterMixCalc()
    c.initiate()
    return c

def test_pcr_calculation_math(calc):
    """
    Verify that the 10% dead volume is calculated correctly.
    Assuming General_PCR has Taq 2X Master Mix: 12.5 uL base
    10 samples * 1.1 = 11.0 total multiplier
    12.5 * 11.0 = 137.5
    """
    result = calc.run("General_PCR", 10)
    
    assert result["Samples"] == 10
    assert result["Scaled Recipe"]["Taq 2X Master Mix"] == 137.5
    assert "Instructions" in result
    assert result["Units"] == "uL"

def test_space_to_underscore_conversion(calc):
    """
    Verify that 'General PCR' is treated the same as 'General_PCR'.
    """
    result = calc.run("General PCR", 5)
    assert result["Protocol"] == "General_PCR"

def test_invalid_protocol_raises_error(calc):
    """
    Verify that ValueError is raised for missing protocols.
    """
    with pytest.raises(ValueError) as excinfo:
        calc.run("Fake_Protocol_99", 5)
    assert "not in the recipe book" in str(excinfo.value)

def test_invalid_sample_count(calc):
    """
    Verify that 0 or negative samples raise an error.
    """
    with pytest.raises(ValueError):
        calc.run("General_PCR", 0)
    with pytest.raises(ValueError):
        calc.run("General_PCR", -1)

def test_instruction_formatting(calc):
    """
    Verify the instruction string correctly injects the volume.
    """
    result = calc.run("General_PCR", 10)
    assert "137.5" in result["Instructions"]