from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet


# routers
router = DefaultRouter()
router.register(r'players', PlayerViewSet)

# urls
urlpatterns = [
    path('', include( router.urls )),

]
