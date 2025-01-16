from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
