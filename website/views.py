from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchForm
from .models				import Sponsor

class IndexView(TemplateView):
    template_name 	= 'website/index.html'

def pages(request):
    sponsors 		= Sponsor.objects.filter(is_active=True).order_by("level", "name")
    porchForm		= PorchForm()
    return render(request, 'website/front-page/index.html', {"sponsors": sponsors, 'form': porchForm})

def call_for_porches(request):
    if request.method == 'POST':
        form = PorchForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'website/call-for-porches/form-thanks.html')
    else:
        form = PorchForm()

    return render(request, 'website/call-for-porches/call-porches.html', {'form': form})

def about(request):
    return render(request, 'website/about.html')