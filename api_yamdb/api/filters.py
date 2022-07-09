from django_filters import rest_framework as filters
from reviews.models import Title


class TitleSearchFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
