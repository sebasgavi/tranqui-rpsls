from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from pprint import pprint

from .models import Player, Game
from .constants import *

# move_a -> move constant
# move_b -> move constant
# returns -1 if winner is a, 1 if winner is b and 0 if is a tie
def get_winner(move_a, move_b):
    if(move_a not in MOVES or move_b not in MOVES):
        return False

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


# Custom Session "Auth" Middleware
class SimplePlayerMiddleware:
    # views that need a logged in player
    protected_views = ['index', 'new', 'leave', 'detail', 'join', 'move_select']
    game_views = ['detail', 'move_select']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # redirect on protected views without player
    def process_view(self, request, view_func, view_args, view_kwargs):
        # get player id from session
        player = request.session.get('player_id', False)
        if(player):
            try:
                # try to load player from db
                player = Player.objects.get(pk=player)
            except Player.DoesNotExist:
                player = False
        
        # pass info to view with the request object
        request.player = player

        # redirect to login if is a protected view and player isn't logged in
        if(not player and view_func.__name__ in self.protected_views):
            return HttpResponseRedirect(reverse('game:login'))

        self.process_game_views(request, view_func, view_args, view_kwargs)

        # else continue
        return None

    def process_game_views(self, request, view_func, view_args, view_kwargs):
        # ignore if not a game view
        if(view_func.__name__ not in self.game_views): return
        # get game_id
        game_id = view_kwargs.get('game_id', False)
        # throw if not game_id  
        if(not game_id): raise Http404()
        # get game
        game = get_object_or_404(Game, pk=game_id)
        # identify player
        which_player = 0
        # player is a
        if(request.player.id == game.player_a.id): which_player = -1
        # player is b
        if(request.player.id == game.player_b.id): which_player = 1
        # player not related, raise 404
        if(which_player == 0): raise Http404() 
        
        # pass game and current player info view
        request.game = game
        request.is_player_a = which_player == -1
        request.is_player_b = which_player == 1