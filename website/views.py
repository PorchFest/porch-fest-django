from django.shortcuts 		import render
from django.views.generic 	import TemplateView

class IndexView(TemplateView):
    template_name = 'website/index.html'

def pages(request):
    return render(request, 'website/pages.html')

def about(request):
    return render(request, 'website/about.html')