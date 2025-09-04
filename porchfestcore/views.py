from django.shortcuts 				import render
from django.views.generic 			import TemplateView
from django.http					import JsonResponse
from django.views.decorators.csrf	import csrf_exempt

def map_page(request):
    return render(request, 'porchfestcore/map.html')


