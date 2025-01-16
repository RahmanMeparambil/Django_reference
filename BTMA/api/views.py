from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Player, Tournament, Matches
from .serializers import PlayerSerializer, TournamentSerializer, MatchesSerializer



# player viewset
class PlayerViewSet( viewsets.ModelViewSet ):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_fields = ['name', 'nationality']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom permission logic:
        - Allow anyone (authenticated or not) to perform read actions (GET).
        - Allow only authenticated users to perform write actions (POST, PUT, PATCH, DELETE).
        """
        if self.action in ['list', 'retrieve']:  
            return [AllowAny()] 
        else:  
            return [IsAuthenticated()]
        
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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom permission logic:
        - Allow anyone (authenticated or not) to perform read actions (GET).
        - Allow only authenticated users to perform write actions (POST, PUT, PATCH, DELETE).
        """
        if self.action in ['list', 'retrieve']:  
            return [AllowAny()] 
        else:  
            return [IsAuthenticated()]

# matches viewset
class MatchesViewSet( viewsets.ModelViewSet ):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Custom permission logic:
        - Allow anyone (authenticated or not) to perform read actions (GET).
        - Allow only authenticated users to perform write actions (POST, PUT, PATCH, DELETE).
        """
        if self.action in ['list', 'retrieve']:  
            return [AllowAny()] 
        else:  
            return [IsAuthenticated()]