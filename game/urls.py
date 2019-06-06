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
    path('detail', views.detail, name='detail')
]