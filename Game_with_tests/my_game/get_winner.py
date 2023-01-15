""""
who are winner
"""
from .options import *


def get_winner(user_val: str, computer_var: str):
    """
    Function that determinate the winner
    :param user_val:
    :param computer_var:
    :return: print message
    """
    MAPPING = {ROCK: SCISSORS, SCISSORS: PAPER, PAPER: ROCK}
    if user_val == computer_var:
        return 'DRAW!'
    elif MAPPING[user_val] == computer_var:
        return 'YOU WIN'
    else:
        return 'YOU LOSE'


def validate_input(user_val: str) -> bool:
    """
    Function that determinate the correct input
    :param user_val:
    :return: bool
    """
    return user_val in OPTIONS
