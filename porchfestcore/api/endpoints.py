from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.http                import JsonResponse
from .serializers               import PorchMapSerializer
from .filters                   import PorchMapFilter
from porchfestcore.models       import Porch

class PorchMap(ListAPIView):
    queryset            = Porch.objects.filter(approved=True).distinct()
    filterset_class     = PorchMapFilter
    serializer_class    = PorchMapSerializer