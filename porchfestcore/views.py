from django.shortcuts 		import render
from django.views.generic 	import TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = 'porchfestcore/index.html'
 
def map_page(request):
    return render(request, 'porchfestcore/map.html')

def pages(request):
    return render(request, 'porchfestcore/pages.html')

def about(request):
    return render(request, 'porchfestcore/about.html')