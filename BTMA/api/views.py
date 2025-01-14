from rest_framework import viewsets
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer
from .filters import PlayerFilter


# player ViewSet
class PlayerViewSet( viewsets.ModelViewSet ):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter


