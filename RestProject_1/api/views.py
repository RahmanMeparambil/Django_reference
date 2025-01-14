from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ItemSerializer,Item,Book,BookSerializer
from rest_framework import viewsets
import django_filters.rest_framework
from api.filters import BookFilter


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name']

class BookViewSet(viewsets.ModelViewSet):
    # filter_backend is added to settings
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter


@api_view(['GET'])
def get_data(request):
    items = Item.objects.all()
    serialize = ItemSerializer(items,many=True)
    return Response(serialize.data)

@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)