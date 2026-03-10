import django_filters
from porchfestcore.models import Porch

class PorchFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='performances__performer__genre', lookup_expr='iexact')

    class Meta:
        model = Porch
        fields = ['genre']