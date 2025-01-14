from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ItemSerializer,Item
from rest_framework import viewsets


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


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