from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('enter', views.enter, name='enter'),
    path('leave', views.leave, name='leave'),
    path('new', views.new, name='new'),
    path('join', views.join, name='join'),
    path('<int:game_id>', views.detail, name='detail'),
    path('<int:game_id>/move', views.move_select, name='move_select'),
    path('<int:game_id>/should_reload', views.should_reload, name='should_reload'),
    path('should_enter_game', views.should_enter_game, name='should_enter_game')
]