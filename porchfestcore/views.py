from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchForm

class IndexView(TemplateView):
	template_name = 'porchfestcore/index.html'
 
def map_page(request):
	return render(request, 'porchfestcore/map.html')

def pages(request):
	return render(request, 'porchfestcore/pages.html')

def call_porches(request):
    if request.method == 'POST':
        form 				= PorchForm(request.POST)
        if form.is_valid():
            porch 			= form.save(commit=False)
            porch.approved 	= False
            porch.save()
            messages.success(request, 'Thank you! Your porch has been submitted for review.')
            return redirect('porch_submitted')
    else:
        form 				= PorchForm()
    return render(request, 'porchfestcore/call-porches.html', {'form': form})

def porch_submitted(request):
    return render(request, 'porchfestcore/porch_submitted.html')