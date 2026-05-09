import pytest
import sys
import os
 
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules', 'labplanner', 'tools'))
from master_mix_calc import calculate_master_mix

def test_pcr_tenfold():
    result = calculate_master_mix("PCR", 10)
    assert result["Scaled Recipe"]["ddH2O"] == round(32.0 * 1.1 * 10, 2)

def test_digest_tenfold():
    result = calculate_master_mix("Digest", 10)
    assert result["Scaled Recipe"]["NEB_Buffer_2_10x"] == round(5 * 10 * 1.1, 2)

def test_ligate_double():
    result = calculate_master_mix("Ligate", 2)
    assert result["Scaled Recipe"]["T4_DNA_ligase"] == round(0.5 * 2 * 1.1, 2)

def test_gibson_triple():
    result = calculate_master_mix("Gibson", 3)
    assert result["Scaled Recipe"]["ddH2O"] == round(6.0 * 3 * 1.1, 2)

def test_golden_gate_fivefold():
    result = calculate_master_mix("Golden_Gate", 5)
    assert result["Scaled Recipe"]["Gibson_Assembly_Master_Mix"] == round(7.5 * 5 * 1.1, 2)

def test_name_without_underscores():
    result = calculate_master_mix("Golden Gate", 3)
    assert result["Protocol"] == "Golden_Gate"

def test_no_samples():
    with pytest.raises(ValueError):
        calculate_master_mix("PCR", 0)

def test_less_than_one_sample():
    with pytest.raises(ValueError):
        calculate_master_mix("PCR", 0.5)

def test_unknown_protocol():
    with pytest.raises(ValueError):
        calculate_master_mix("Lancelot", 5)

def num_samples_not_int():
    with pytest.raises(ValueError):
        calculate_master_mix("PCR", "Lancelot")

