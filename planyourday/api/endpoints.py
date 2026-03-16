from rest_framework.generics    import ListAPIView
from .serializers               import PerformanceSerializer
from .filters                   import PerformanceFilter
from porchfestcore.models       import Performance

class Performances(ListAPIView):
    queryset            = Performance.objects.filter(porch__approved=True).distinct()
    filterset_class     = PerformanceFilter
    serializer_class    = PerformanceSerializer