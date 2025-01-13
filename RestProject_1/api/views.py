from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['GET'])
def get_data(request):
    data = {'name':'Rahman','age':26}
    return Response(data)