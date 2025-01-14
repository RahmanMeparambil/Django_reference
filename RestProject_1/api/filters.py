import django_filters
from base.models import Book

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'name':['iexact', 'contains'],
            'pages':['lt', 'gt'],
        }