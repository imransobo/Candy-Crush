from pyexpat import model
from tkinter import CASCADE
from django.db import models

# Create your models here.

class Player(models.Model):
    player_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()


