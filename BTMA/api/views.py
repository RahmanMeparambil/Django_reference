from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .permission import IsAdminOrReadOnly
from .models import Player, Tournament, Matches
from .serializers import PlayerSerializer, TournamentSerializer, MatchesSerializer



# player viewset
@extend_schema(
    tags=["Players"],
    description="Create, retrieve, and list players. You can also search players by name and nationality.",
    responses={
        200: PlayerSerializer,  
        400: OpenApiResponse(description="Bad Request - Invalid parameters"),
        404: OpenApiResponse(description="Not Found - Player does not exist")
    },
    request=PlayerSerializer,  
)
class PlayerViewSet( viewsets.ModelViewSet ):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_fields = ['name', 'nationality']
    permission_classes = [IsAdminOrReadOnly]
        
# ranking viewset
@extend_schema(
    tags=["Rankings"],
    description="Retrieve the list of players sorted by ranking points in descending order.",
    responses={
        200: PlayerSerializer,  
        404: OpenApiResponse(description="Not Found - No players found")
    },
)
class PlayerRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all().order_by('-ranking_points')
    serializer_class = PlayerSerializer

# tournament viewset
@extend_schema(
    tags=["Tournaments"],
    description="Create, update, retrieve, and list tournaments. You can search tournaments by name.",
    responses={
        200: TournamentSerializer,  
        400: OpenApiResponse(description="Bad Request - Invalid tournament data"),
        404: OpenApiResponse(description="Not Found - Tournament does not exist")
    },
    request=TournamentSerializer,  
)
class TournamentViewSet( viewsets.ModelViewSet ):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]

# matches viewset
@extend_schema(
    tags=["Matches"],
    description="Create, update, retrieve, and list matches in a tournament.",
    responses={
        200: MatchesSerializer,  
        400: OpenApiResponse(description="Bad Request - Invalid match data"),
        404: OpenApiResponse(description="Not Found - Match does not exist")
    },
    request=MatchesSerializer,  
)
class MatchesViewSet( viewsets.ModelViewSet ):
    queryset = Matches.objects.all()
    serializer_class = MatchesSerializer            
    permission_classes = [IsAdminOrReadOnly]
