from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchInterestForm, PorchSignupForm
from .models				import Sponsor

def index(request):
    sponsors 		= Sponsor.objects.filter(is_active=True).order_by("level", "name")
    form		= PorchSignupForm()
    return render(request, 'website/front-page/index.html', {"sponsors": sponsors, 'form': form})

def porch_signup(request):
    if request.method == 'POST':
        form = PorchSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'website/porch-signup-page/success.html')
    else:
        form = PorchSignupForm()

    return render(request, 'website/porch-signup-page/porch-signup.html', {'form': form})

def porch_list_signup(request):
    if request.method == 'POST':
        form = PorchInterestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'website/porch-list-form/success.html')
    else:
        form = PorchInterestForm()

    return render(request, 'website/porch-list-form/porch-list-form.html', {'form': form})

def about(request):
    return render(request, 'website/about.html')