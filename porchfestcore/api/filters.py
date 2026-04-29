import django_filters
from porchfestcore.models   import Porch, Genre
from django.db.models       import Q
from planyourday.views      import get_or_create_itinerary

class PorchMapFilter(django_filters.FilterSet):
    search          = django_filters.CharFilter(method="filter_search")
    genres          = django_filters.MultipleChoiceFilter(
        field_name='performances__performer__genres__slug',
        choices=[],
    )
    after           = django_filters.TimeFilter(
        field_name  ='performances__start_time',
        lookup_expr ='gte'
    )
    vendor          = django_filters.BooleanFilter(field_name='vendor')
    sponsored       = django_filters.BooleanFilter(field_name='sponsored')
    number          = django_filters.NumberFilter(field_name='number')
    childrens_activities = django_filters.BooleanFilter(field_name='childrens_activities')
    itinerary       = django_filters.BooleanFilter(method="filter_itinerary")
    porta_potty       = django_filters.BooleanFilter(field_name='porta_potty')
    class Meta:
        model       = Porch
        fields      = ['genres', 'after', 'vendor', 'sponsored', 'number', 'itinerary']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['genres'].extra['choices'] = [
            (g.slug, g.name) for g in Genre.objects.all()
        ]
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(performances__performer__name__icontains=value) |
            Q(street_address__icontains=value)
        )
    def filter_itinerary(self, queryset, name, value):
        if not value:
            return queryset
        itinerary_id = self.request.session.get("itinerary_id")
        if not itinerary_id:
            return queryset.none()
        itinerary = get_or_create_itinerary(self.request)
        if not itinerary:
            return queryset.none()
        return queryset.filter(
            performances__in=itinerary.performances.all()
        )