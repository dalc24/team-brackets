# test_bracket.py
import pytest
from bracket import Bracket

"""
tests for setting number of teams 
"""
def test_set_teams_4():
    bracket = Bracket()
    bracket.set_teams(4)  
    assert len(bracket.get_teams()) == 4 

def test_set_teams_8():
    bracket = Bracket()
    bracket.set_teams(8)  
    assert len(bracket.get_teams()) == 8

def test_set_teams_32():
    bracket = Bracket()
    bracket.set_teams(32)  
    assert len(bracket.get_teams()) == 32

def test_set_invalid_teams_less_than():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.set_teams(3)  


def test_set_invalid_teams_greater_than():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.set_teams(64)

def test_set_invalid_teams_not_power2():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.set_teams(6)

