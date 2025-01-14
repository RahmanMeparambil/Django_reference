import django_filters
from .models import Player


class PlayerFilter(django_filters.FilterSet):
    class Meta:
        model = Player
        fields = {
            'name':[ 'iexact', 'icontains' ],
            'nationality':[ 'iexact', 'icontains' ],
        }