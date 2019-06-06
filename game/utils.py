from .constants import *

def get_winner(move_a, move_b):
    if(move_a not in MOVES or move_b not in MOVES):
        raise Exception('invalid move')

    if move_a == SCISSORS and (move_b == PAPER or move_b == LIZARD):
        return -1
    elif move_a == PAPER and (move_b == ROCK or move_b == SPOCK):
        return -1
    elif move_a == ROCK and (move_b == LIZARD or move_b == SCISSORS):
        return -1
    elif move_a == LIZARD and (move_b == SPOCK or move_b == PAPER):
        return -1
    elif move_a == SPOCK and (move_b == SCISSORS or move_b == ROCK):
        return -1
    elif move_a == move_b:
        return 0
    else:
        return 1