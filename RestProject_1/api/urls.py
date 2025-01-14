from django.urls import path, include
from .views import get_data,addItem
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,BookViewSet


# router
router = DefaultRouter()
router.register(r'items', ItemViewSet) 
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', get_data),
    path('add/',addItem),
    path('router/',include(router.urls)),
]
