from rest_framework import viewsets
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer
from .filters import PlayerFilter, TournamentFilter


# player viewset
class PlayerViewSet( viewsets.ModelViewSet ):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter

# ranking viewset
class PlayerRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all().order_by('-ranking_points')
    serializer_class = PlayerSerializer
    filterset_class = PlayerFilter 


# tournament viewset
class TournamentViewSet( viewsets.ModelViewSet ):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filterset_class = TournamentFilter