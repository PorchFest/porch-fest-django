from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from django.http			import JsonResponse
from django.conf 		    import settings
from .models                import Genre

def map_page(request):
    genres = Genre.objects.all()
    return render(request, 'porchfestcore/map.html', {
        'genres': genres,
        'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY
    })


