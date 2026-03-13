import django_filters
from porchfestcore.models   import Porch
from django.db.models       import Q

class PorchMapFilter(django_filters.FilterSet):
    search          = django_filters.CharFilter(method="filter_search")
    genre           = django_filters.CharFilter(
        field_name  ='performances__performer__genre',
        lookup_expr ='iexact'
    )
    after           = django_filters.TimeFilter(
        field_name  ='performances__start_time',
        lookup_expr ='gte'
    )
    vendor          = django_filters.BooleanFilter(field_name='vendor')
    sponsored       = django_filters.BooleanFilter(field_name='sponsored')
    class Meta:
        model       = Porch
        fields      = ['genre', 'after', 'vendor', 'sponsored']
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(performances__performer__name__icontains=value)
        )