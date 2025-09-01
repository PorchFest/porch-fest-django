from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchForm


 
def map_page(request):
    return render(request, 'porchfestcore/map.html')
