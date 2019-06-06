from django.test import TestCase

from .constants import *
from .utils import get_winner

class GetWinnerUtilTests(TestCase):
    def test_game_posibilities(self):
        # a player wins
        self.assertIs(get_winner(SCISSORS, PAPER), -1)
        self.assertIs(get_winner(PAPER, ROCK), -1)
        self.assertIs(get_winner(ROCK, LIZARD), -1)
        self.assertIs(get_winner(LIZARD, SPOCK), -1)
        self.assertIs(get_winner(SPOCK, SCISSORS), -1)
        self.assertIs(get_winner(SCISSORS, LIZARD), -1)
        self.assertIs(get_winner(LIZARD, PAPER), -1)
        self.assertIs(get_winner(PAPER, SPOCK), -1)
        self.assertIs(get_winner(SPOCK, ROCK), -1)
        self.assertIs(get_winner(ROCK, SCISSORS), -1)
        # b player wins
        self.assertIs(get_winner(PAPER, SCISSORS), 1)
        self.assertIs(get_winner(ROCK, PAPER), 1)
        self.assertIs(get_winner(LIZARD, ROCK), 1)
        self.assertIs(get_winner(SPOCK, LIZARD), 1)
        self.assertIs(get_winner(SCISSORS, SPOCK), 1)
        self.assertIs(get_winner(LIZARD, SCISSORS), 1)
        self.assertIs(get_winner(PAPER, LIZARD), 1)
        self.assertIs(get_winner(SPOCK, PAPER), 1)
        self.assertIs(get_winner(ROCK, SPOCK), 1)
        self.assertIs(get_winner(SCISSORS, ROCK), 1)
        # tie
        self.assertIs(get_winner(ROCK, ROCK), 0)
        self.assertIs(get_winner(PAPER, PAPER), 0)
        self.assertIs(get_winner(SCISSORS, SCISSORS), 0)
        self.assertIs(get_winner(LIZARD, LIZARD), 0)
        self.assertIs(get_winner(SPOCK, SPOCK), 0)