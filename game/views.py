from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Player, Game
from .constants import *

def index(request):
    context = {
        'player': request.player
    }
    return render(request, 'game/index.html', context=context)


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


def leave(request):
    # remove info from session if exists
    if('player_id' in request.session):
        del request.session['player_id']
    # redirect to game index
    return HttpResponseRedirect(reverse('game:index'))


def new(request):
    game = Game(player_a=request.player, steps='[]')
    game.save()
    context = {
        'player': request.player,
        'game': game
    }
    return HttpResponseRedirect(reverse('game:field'))


def field(request):
    context = {
        'player': request.player
    }
    return render(request, 'game/field.html', context=context)