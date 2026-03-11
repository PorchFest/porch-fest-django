from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.http                import JsonResponse
from .serializers               import PorchesSerializer
from .filters                   import PorchFilter
from porchfestcore.models       import Porch

class PorchMap(ListAPIView):
    queryset            = Porch.objects.filter(approved=True).distinct()
    serializer_class    = PorchesSerializer
    filterset_class     = PorchFilter