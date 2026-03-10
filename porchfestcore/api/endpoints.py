from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.http                import JsonResponse
from .serializers               import PorchesSerializer
from .filters                   import PorchFilter
from porchfestcore.models       import Porch

class Porches(ListAPIView):
    queryset = Porch.objects.filter(approved=True).distinct()
    serializer_class = PorchesSerializer
    filterset_class = PorchFilter

# class Porches(APIView):
#     def get(self, request, *args, **kwargs):
#         genre       = request.GET.get('genre')
#         # porches     = Porch.objects.all()
#         porches     = Porch.objects.filter(
#             performances__performer__genre=genre
#         ).distinct()
#         print(porches)
#         serializer  = PorchesSerializer(porches, many=True)
#         data        = serializer.data
#         return JsonResponse(data, safe=False)