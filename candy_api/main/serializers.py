from rest_framework import serializers
from . import models


class PlayerListSerializer(serializers.ModelSerializer):
     class Meta:
        model = models.Player
        fields = ['id','player_name','email','password']

class ScoreListSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Score
      fields = ['id', 'player', 'score']


class ScoreBoardSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Score
      fields = ['id', 'player', 'score']
      depth = 1