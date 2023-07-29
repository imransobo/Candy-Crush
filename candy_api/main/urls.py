

from django import views

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('player/', views.PlayerList.as_view()),
    path('login', views.user_login),
    path('scores/', views.ScoreList.as_view()),
    path('scoreboard/', views.ScoreBoard.as_view()),
    path('player/<int:pk>', views.PlayerDetails.as_view()),
    path('forgot-password', views.reset_user_pass),
    
    
]