import django_filters
from .models import Player, Tournament


class PlayerFilter(django_filters.FilterSet):
    class Meta:
        model = Player
        fields = {
            'name':['iexact', 'icontains' ],
            'nationality':['iexact', 'icontains' ],
        }

class TournamentFilter(django_filters.FilterSet):
    class Meta:
        model = Tournament
        fields = {
            'name':['iexact', 'icontains' ],
        }