from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, PlayerRankingViewSet, TournamentViewSet, MatchesViewSet


# routers
router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'rankings', PlayerRankingViewSet, basename='ranking') # Unique basename for PlayerRankingViewSet
router.register(r'tournaments', TournamentViewSet)
router.register(r'matches', MatchesViewSet)

# urls
urlpatterns = [
    path('', include( router.urls )),
]
