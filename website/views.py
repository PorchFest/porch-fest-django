from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from porchfestcore.forms	import PorchForm
from .models				import Sponsor

class IndexView(TemplateView):
    template_name 	= 'website/index.html'

def pages(request):
    sponsors 		= Sponsor.objects.filter(is_active=True).order_by("level", "name")
    porchForm		= PorchForm()
    return render(request, 'website/front-page/index.html', {"sponsors": sponsors, 'form': porchForm})

def about(request):
    return render(request, 'website/about.html')