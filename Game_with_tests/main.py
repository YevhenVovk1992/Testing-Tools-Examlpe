from random import choice
from my_game.get_winner import get_winner, validate_input
from my_game.options import *


# Game loop
print('', 'Welcome to ma game!', sep='\t')
print('', '!-----------------!', sep='\t')
while True:
    user_val = input(f'Type one of the values: {", ".join(OPTIONS)} \n')
    if user_val == 'end':
        print('', 'Good luck :)', sep='\t')
        break
    elif not validate_input(user_val):
        print('Wrong value. Try again.')
        continue
    computer_var = choice(OPTIONS)
    print('Computer value:', computer_var)
    print(get_winner(user_val, computer_var))
    print('If you want to exit, type "end"')
    print('-   -   -   -   -   -   -   -')
