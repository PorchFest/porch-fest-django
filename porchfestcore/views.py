from django.shortcuts 				import render
from django.views.generic 			import TemplateView
from django.http					import JsonResponse
from django.views.decorators.csrf	import csrf_exempt
from .models                        import Porch, Performer

def map_page(request):
    genres = Performer.Genre.choices
    return render(request, 'porchfestcore/map.html', {'genres': genres})


