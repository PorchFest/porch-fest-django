import django_filters
from porchfestcore.models   import Porch, Genre
from django.db.models       import Q

class PorchMapFilter(django_filters.FilterSet):
    search          = django_filters.CharFilter(method="filter_search")
    genres          = django_filters.MultipleChoiceFilter(
        field_name='performances__performer__genres__slug',
        choices=[],  # placeholder
    )
    after           = django_filters.TimeFilter(
        field_name  ='performances__start_time',
        lookup_expr ='gte'
    )
    vendor          = django_filters.BooleanFilter(field_name='vendor')
    sponsored       = django_filters.BooleanFilter(field_name='sponsored')
    class Meta:
        model       = Porch
        fields      = ['genres', 'after', 'vendor', 'sponsored']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['genres'].extra['choices'] = [
            (g.slug, g.name) for g in Genre.objects.all()
        ]
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(performances__performer__name__icontains=value)
        )