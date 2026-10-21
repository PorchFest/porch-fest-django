from django.shortcuts 		import render
from django.views.generic 	import TemplateView, ListView
from django.http			import JsonResponse
from django.conf 		    import settings
from .models                import Genre, Performer
from planyourday.views      import get_or_create_itinerary

def map_page(request):
    genres = Genre.objects.order_by('name').filter(performer__isnull=False).distinct()
    context = {
        'genres': genres,
        'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY
    }
    if request.session.get('itinerary_id'):
        context['itinerary'] = get_or_create_itinerary(request).ordered_performances()

    return render(request, 'porches/map.html', context)

class PerformerListView(ListView):
    template_name = 'performer-signup-page/performer-list.html'
    context_object_name = 'performers'

    def get_queryset(self):
        q = self.request.GET.get("name", "").strip()

        if not q:
            return Performer.objects.none()

        return Performer.objects.filter(name__icontains=q)

def bland_map(request):
    return render(request, 'porches/bland-map.html', {'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY})

def coming_soon(request):
    return render(request, 'porches/coming-soon.html')