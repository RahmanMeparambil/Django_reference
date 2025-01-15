from rest_framework import serializers
from .models import Player, Tournament


class PlayerSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Player
        fields = '__all__'

class TournamentSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Tournament
        fields = '__all__'

class PlayerSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Player
        fields = '__all__'