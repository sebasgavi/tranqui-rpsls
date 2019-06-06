from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from pprint import pprint


from .models import Player, Game
from .constants import MOVES

# player dashboard view
def index(request):
    player = request.player
    context = {
        'player': player,
        'other_new_games': Game.objects.filter(~Q(player_a=player.id), ~Q(player_b=player.id)),
        'own_games': player.own_games.all()
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
        raise Http404()
    # set player_b
    request.player.other_games.add(game)
    request.player.current_games.add(game)
    return HttpResponseRedirect(reverse('game:detail', kwargs={ 'game_id': game.id }))


# game detail view
def detail(request, game_id):
    player = request.player
    game = get_object_or_404(Game, pk=game_id)
    if(player.id != game.player_a.id and player.id != game.player_b.id):
        raise Http404()
    context = {
        'player': request.player,
        'game': game,
        'moves': MOVES
    }
    return render(request, 'game/detail.html', context=context)