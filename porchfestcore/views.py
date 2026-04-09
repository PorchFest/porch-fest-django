from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from django.http			import JsonResponse
from django.conf 		    import settings
from .models                import Genre
from planyourday.views import get_or_create_itinerary

def map_page(request):
    genres = Genre.objects.filter(performer__isnull=False).distinct()
    context = {
        'genres': genres,
        'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY
    }
    if request.session.get('itinerary_id'):
        context['itinerary'] = get_or_create_itinerary(request).ordered_performances()

    return render(request, 'porchfestcore/map.html', context)