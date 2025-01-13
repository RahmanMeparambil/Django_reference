from django.urls import path
from .views import get_data,addItem

urlpatterns = [
    path('', get_data),
    path('add/',addItem),
]
