from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Player

def index(request):
    player = request.session.get('player_id', False)
    if(player):
        try:
            player = Player.objects.get(pk=player)
        except Player.DoesNotExist:
            player = false
    context = {
        'player': player
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