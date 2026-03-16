import django_filters
from porchfestcore.models   import Performance
from django.db.models       import Q

class PerformanceFilter(django_filters.FilterSet):
    search          = django_filters.CharFilter(method="filter_search")
    genre           = django_filters.CharFilter(
        field_name  ='performer__genre',
        lookup_expr ='iexact'
    )
    class Meta:
        model       = Performance
        fields      = ['genre',]
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(performer__name__icontains=value) |
            Q(porch__name__icontains=value)
        )