import django_filters
from src.apps.porchfestcore.models   import Performance, Genre
from django.db.models       import Q

class PerformanceFilter(django_filters.FilterSet):
    search          = django_filters.CharFilter(method="filter_search")
    genres          = django_filters.MultipleChoiceFilter(
        field_name='performer__genres__slug',
        choices=[],
    )
    after           = django_filters.TimeFilter(
        field_name  ='start_time',
        lookup_expr ='gte'
    )
    number          = django_filters.NumberFilter(field_name='porch__number')
    class Meta:
        model   = Performance
        fields  = ['genres', 'number']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['genres'].extra['choices'] = [
            (g.slug, g.name) for g in Genre.objects.all()
        ]
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(performer__name__icontains=value) |
            Q(porch__name__icontains=value) |
            Q(porch__street_address__icontains=value)
        )