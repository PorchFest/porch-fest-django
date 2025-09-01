from django.shortcuts 		import render
from django.views.generic 	import TemplateView

# Create your views here.


 
def map_page(request):
    return render(request, 'porchfestcore/map.html')