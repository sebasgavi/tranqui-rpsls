from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Player
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


class SimplePlayerMiddleware:
    protected_views = ['new', 'field']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        player = request.session.get('player_id', False)
        if(player):
            try:
                player = Player.objects.get(pk=player)
            except Player.DoesNotExist:
                player = False
        
        request.player = player

        if(not player and view_func.__name__ in self.protected_views):
            return HttpResponseRedirect(reverse('game:index'))

        return None