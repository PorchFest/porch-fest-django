import django_filters
from porchfestcore.models import Porch

class PorchFilter(django_filters.FilterSet):
    genre       = django_filters.CharFilter(
        field_name='performances__performer__genre',
        lookup_expr='iexact'
    )
    after       = django_filters.TimeFilter(
        field_name='performances__start_time',
        lookup_expr='gte'
    )
    vendor      = django_filters.BooleanFilter(field_name='vendor')
    sponsored   = django_filters.BooleanFilter(field_name='sponsored')

    class Meta:
        model   = Porch
        fields  = ['genre', 'after', 'vendor', 'sponsored']