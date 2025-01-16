from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .permission import IsAdminOrReadOnly
from .models import Player, Tournament, Matches
from .serializers import PlayerSerializer, TournamentSerializer, MatchesSerializer



# player viewset
class PlayerViewSet( viewsets.ModelViewSet ):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_fields = ['name', 'nationality']
    permission_classes = [IsAdminOrReadOnly]
        
# ranking viewset
class PlayerRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all().order_by('-ranking_points')
    serializer_class = PlayerSerializer

# tournament viewset
class TournamentViewSet( viewsets.ModelViewSet ):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]

# matches viewset
class MatchesViewSet( viewsets.ModelViewSet ):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer
    permission_classes = [IsAdminOrReadOnly]
