from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchInterestForm, PorchSignupForm
from .models				import Sponsor
from porchfestcore.models   import TempUpload

def index(request):
    sponsors 		= Sponsor.objects.filter(is_active=True).order_by("level", "name")
    form		= PorchSignupForm()
    return render(request, 'website/front-page/index.html', {"sponsors": sponsors, 'form': form})

def porch_signup(request):
    temp_image = None
    if request.method == 'POST':
        if "porch_picture" in request.FILES:
            temp_image = TempUpload.objects.create(
                image=request.FILES["porch_picture"]
            )
        elif request.POST.get("temp_image_id"):
            temp_image = TempUpload.objects.filter(
                id=request.POST["temp_image_id"]
            ).first()
        form = PorchSignupForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if temp_image:
                instance.porch_picture = temp_image.image
                temp_image.delete()
            instance.save()
            return render(request, 'website/porch-signup-page/success.html')
    else:
        form = PorchSignupForm()

    return render(request, 'website/porch-signup-page/porch-signup.html', {
        'form': form,
        "temp_image": temp_image,
    })

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