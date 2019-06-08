from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
import json
from pprint import pprint

from .models import Player, Game
from .constants import MOVES
from .utils import get_game_results

# player dashboard view
def index(request):
    player = request.player
    # related games ordered by winner value exists
    games = (player.own_games.all() | player.other_games.all()).order_by('winner')
    # new games of other players to join
    other_new_games = Game.objects.filter(~Q(player_a=player.id), player_b__isnull=True)
    error = request.GET.get('error', False)
    context = {
        'player': player,
        'other_new_games': other_new_games,
        'own_games': games,
        'error_game_full': True if error == 'game_full' else False
    }
    return render(request, 'game/index.html', context=context)


# login form view
def login(request):
    if(request.player):
        return HttpResponseRedirect(reverse('game:index'))
    return render(request, 'game/login.html')


# login form action
def enter(request):
    # get name from form
    name = request.POST['name']
    # if name exists try to get player or create a new one
    if(name):
        try:
            player = Player.objects.get(name=name)
        except Player.DoesNotExist:
            player = Player(name=name)
            player.save()
        # save player id in session
        request.session['player_id'] = player.id
    # redirect to game index
    return HttpResponseRedirect(reverse('game:index'))


# logout form action
def leave(request):
    # remove info from session if exists
    if('player_id' in request.session):
        del request.session['player_id']
    # redirect to game index
    return HttpResponseRedirect(reverse('game:index'))


# new game action
def new(request):
    game = Game(player_a=request.player, steps='[]')
    game.save()
    return HttpResponseRedirect(reverse('game:index'))


# join game action
def join(request):
    game = get_object_or_404(Game, pk=request.POST['game_id'])
    # game full
    if(game.player_b_id):
        return HttpResponseRedirect(reverse('game:index') + "?error=game_full")    
    # set player_b
    request.player.other_games.add(game)
    return HttpResponseRedirect(reverse('game:detail', kwargs={ 'game_id': game.id }))


# player reload action when 
def should_reload(request, game_id):
    game = request.game
    my_turn = "true" if not game.move_a and not game.move_b else "false"
    return HttpResponse(my_turn)

# game detail view
def detail(request, game_id):
    game = request.game
    if(request.player.id != game.player_a.id
        and request.player.id != game.player_b.id):
        raise Http404()
    context = {
        'player': request.player,
        'game': game,
        'moves': MOVES,
        'steps': json.loads(game.steps),
        'already_played': (request.is_player_a and game.move_a) or (request.is_player_b and game.move_b),
        'other_player': game.player_b if request.is_player_a else game.player_a
    }
    return render(request, 'game/detail.html', context=context)


# game move select action
def move_select(request, game_id):
    game = request.game
    # get move
    selected_move = request.POST.get('move', False)
    # verify valid move
    if(selected_move not in MOVES): raise Http404()
    # set move_a for player_a
    if(request.is_player_a and not game.move_a):
        game.move_a = selected_move
    # set move_b for player_b
    elif(request.is_player_b and not game.move_b):
        game.move_b = selected_move
    # move already selected
    else: raise Http404()

    # maybe get game result
    result = get_game_results(game.move_a, game.move_b)
    # if both played already
    if(result is not False):
        # if game ended
        if(result is not 0):
            # set winner
            game.winner_id = game.player_a.id if result == -1 else game.player_b.id
        # parse steps
        steps = json.loads(game.steps)
        # append last play
        steps.append([ game.move_a, game.move_b, result ])
        # save updated steps
        game.steps = json.dumps(steps)
        # clean moves
        game.move_a = ''
        game.move_b = ''

    # save game moves, steps and winner
    game.save()
    # redirect to detail
    return HttpResponseRedirect(reverse('game:detail', kwargs={ 'game_id': game.id }))