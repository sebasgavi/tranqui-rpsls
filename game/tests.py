from django.test import TestCase

from .constants import *
from .utils import get_game_results

class GetWinnerUtilTests(TestCase):
    def test_game_posibilities(self):
        # a player wins
        self.assertIs(get_game_results(SCISSORS, PAPER), -1)
        self.assertIs(get_game_results(PAPER, ROCK), -1)
        self.assertIs(get_game_results(ROCK, LIZARD), -1)
        self.assertIs(get_game_results(LIZARD, SPOCK), -1)
        self.assertIs(get_game_results(SPOCK, SCISSORS), -1)
        self.assertIs(get_game_results(SCISSORS, LIZARD), -1)
        self.assertIs(get_game_results(LIZARD, PAPER), -1)
        self.assertIs(get_game_results(PAPER, SPOCK), -1)
        self.assertIs(get_game_results(SPOCK, ROCK), -1)
        self.assertIs(get_game_results(ROCK, SCISSORS), -1)
        # b player wins
        self.assertIs(get_game_results(PAPER, SCISSORS), 1)
        self.assertIs(get_game_results(ROCK, PAPER), 1)
        self.assertIs(get_game_results(LIZARD, ROCK), 1)
        self.assertIs(get_game_results(SPOCK, LIZARD), 1)
        self.assertIs(get_game_results(SCISSORS, SPOCK), 1)
        self.assertIs(get_game_results(LIZARD, SCISSORS), 1)
        self.assertIs(get_game_results(PAPER, LIZARD), 1)
        self.assertIs(get_game_results(SPOCK, PAPER), 1)
        self.assertIs(get_game_results(ROCK, SPOCK), 1)
        self.assertIs(get_game_results(SCISSORS, ROCK), 1)
        # tie
        self.assertIs(get_game_results(ROCK, ROCK), 0)
        self.assertIs(get_game_results(PAPER, PAPER), 0)
        self.assertIs(get_game_results(SCISSORS, SCISSORS), 0)
        self.assertIs(get_game_results(LIZARD, LIZARD), 0)
        self.assertIs(get_game_results(SPOCK, SPOCK), 0)