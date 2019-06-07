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
    path('<int:game_id>/is_my_turn', views.is_my_turn, name='is_my_turn')
]