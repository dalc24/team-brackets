# test_bracket.py
import pytest
from bracket import Bracket


"""
initialization test
"""
def test_brackek_init():
    bracket = Bracket()
    assert bracket.teams == []
    assert bracket.winners == []

"""
tests for setting number of teams 
"""
def test_set_teams_4():
    bracket = Bracket()
    bracket.setNumberTeams(4)  
    assert len(bracket.teams) == 4 

def test_set_teams_8():
    bracket = Bracket()
    bracket.setNumberTeams(8)  
    assert len(bracket.teams) == 8

def test_set_invalid_teams_less_than():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.setNumberTeams(3)  


def test_set_invalid_teams_greater_than():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.setNumberTeams(64)

def test_set_invalid_teams_not_power2():
    bracket = Bracket()
    with pytest.raises(ValueError):
        bracket.setNumberTeams(6)

"""
tests for setting names
"""

def test_set_names_valid_4():
    bracket = Bracket()
    bracket.setNumberTeams(4)  
    bracket.setTeamNames(0, "Team A")
    bracket.setTeamNames(1, "Team B")
    assert bracket.teams[1] =="Team B"

def test_set_names_valid_8():
    bracket = Bracket()
    bracket.setNumberTeams(8)  
    bracket.setTeamNames(0, "1")
    bracket.setTeamNames(1, "2")
    bracket.setTeamNames(2, "3")
    bracket.setTeamNames(3, "4")
    bracket.setTeamNames(4, "5")
    bracket.setTeamNames(5, "6")
    bracket.setTeamNames(6, "7")
    bracket.setTeamNames(7, "8")
    assert bracket.teams[6] == "7"

def test_set_names_invalid_4():
    bracket = Bracket()
    bracket.setNumberTeams(4)  
    with pytest.raises(IndexError):
        bracket.setTeamNames(0, "1")
        bracket.setTeamNames(1, "2")
        bracket.setTeamNames(3, "3")
        bracket.setTeamNames(5, "4")
        bracket.setTeamNames(2, "5")

"""
tests for get names
"""
def test_get_names_valid():
    bracket = Bracket()
    bracket.setNumberTeams(4)  
    bracket.setTeamNames(0, "Team A")
    bracket.setTeamNames(1, "Team B")
    bracket.setTeamNames(2, "Team C")
    bracket.setTeamNames(3, "Team D")
    assert bracket.getTeamNames() == ["Team A", "Team B", "Team C", "Team D"]

def test_get_names_valid2():
    bracket = Bracket()
    bracket.setNumberTeams(8)  
    bracket.setTeamNames(7, "Team Z")
    assert bracket.getTeamNames() == [None, None, None, None, None, None, None, "Team Z"]

"""
tests for createBracket
"""
def test_createBracket():
    bracket = Bracket()
    bracket.setNumberTeams(8)

    for i in range(8):
        bracket.setTeamNames(i, f"Team {i+1}")
    
    leftSide, rightSide = bracket.createBracket()
    
    assert len(leftSide) == 4
    assert len(rightSide) == 4
    assert len(leftSide + rightSide) == 8
    assert set(leftSide + rightSide) == set(bracket.getTeamNames())

"""
tests for chooseWinners
"""
def test_chooseWinners_valid(monkeypatch):
    bracket = Bracket()
    teams = ["Team 1", "Team 2", "Team 3", "Team 4"]

    inputs = iter(["Team 1", "Team 3"])  # Simulated input
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    winners = bracket.chooseWinners(teams)
    assert winners == ["Team 1", "Team 3"]

def test_chooseWinners_invalid_input(monkeypatch):
    bracket = Bracket()
    teams = ["Team 1", "Team 2", "Team 3", "Team 4"]

    inputs = iter([ "Invalid Team", "Team 1", "Wrong Team", "Team 4" ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    winners = bracket.chooseWinners(teams)

    assert winners == ["Team 1", "Team 4"]
