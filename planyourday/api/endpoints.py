from rest_framework.generics    import ListAPIView
from django.http import JsonResponse
from .serializers               import PerformanceSerializer
from .filters                   import PerformanceFilter
from porchfestcore.models       import Performance
from planyourday.models         import Itinerary
from django.views.decorators.csrf import csrf_exempt

class Performances(ListAPIView):
    queryset            = Performance.objects.filter(porch__approved=True).distinct()
    filterset_class     = PerformanceFilter
    serializer_class    = PerformanceSerializer

def create_itinerary(request):
    itinerary = Itinerary.objects.create()
    return JsonResponse({'itinerary_id': str(itinerary.id)})

def get_itinerary(request, itinerary_id):
    try:
        itinerary       = Itinerary.objects.get(id=itinerary_id)
        performances    = itinerary.ordered_performances()
        # This is a placeholder for conflict detection logic. The idea is to annotate each performance with a boolean indicating whether it conflicts with any other performance in the itinerary. This would allow the frontend to visually indicate conflicts.
        # conflicts = itnerary.performances.filter(
        #     start_time__lt=models.OuterRef('end_time'),
        #     end_time__gt=models.OuterRef('start_time')
        # )
        # performances = performances.annotate(
        #     has_conflict=models.Exists(conflicts)
        # )
        serializer      = PerformanceSerializer(performances, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': 'Itinerary not found'}, status=404)

@csrf_exempt
def add_performance(request, itinerary_id):
    try:
        itinerary       = Itinerary.objects.get(id=itinerary_id)
        performance_id  = request.POST.get('performance_id')
        print(performance_id)
        performance     = Performance.objects.get(id=performance_id)
        if itinerary.performances.filter(id=performance.id).exists():
            return JsonResponse({'error': 'Performance already in itinerary'}, status=400)
        itinerary.performances.add(performance)
        return JsonResponse({'message': 'Performance added to itinerary'})
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': 'Itinerary not found'}, status=404)
    except Performance.DoesNotExist:
        return JsonResponse({'error': 'Performance not found'}, status=404)

@csrf_exempt
def remove_performance(request, itinerary_id):
    try:
        itinerary       = Itinerary.objects.get(id=itinerary_id)
        performance_id  = request.POST.get('performance_id')
        performance     = Performance.objects.get(id=performance_id)
        if not itinerary.performances.filter(id=performance.id).exists():
            return JsonResponse({'error': 'Performance not in itinerary'}, status=400)
        itinerary.performances.remove(performance)
        return JsonResponse({'message': 'Performance removed from itinerary'})
    except Itinerary.DoesNotExist:
        return JsonResponse({'error': 'Itinerary not found'}, status=404)
    except Performance.DoesNotExist:
        return JsonResponse({'error': 'Performance not found'}, status=404)