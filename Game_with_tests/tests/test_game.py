"""
    User input validation test and test get winner
"""
from Game_with_tests.my_game.get_winner import validate_input, get_winner


def test_valid_input_0():
    assert validate_input('rock') == True

def test_valid_input_1():
    assert validate_input('scissiors') == True

def test_valid_input_2():
    assert validate_input('hello') == False

def test_valid_input_3():
    assert validate_input(32) == False

def test_get_winner_0():
    assert get_winner('rock', 'rock') == 'DRAW!'

def test_get_winner_1():
    assert get_winner('paper', 'rock') == 'YOU WIN'

def test_get_winner_2():
    assert get_winner('scissiors', 'rock') == 'YOU LOSE'
