from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Player, Tournament, Match
from .serializers import PlayerSerializer, TournamentSerializer
from .filters import PlayerFilter


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
    filter_backends = (SearchFilter,)
    search_fields = ['name']