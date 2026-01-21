from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from .forms					import PorchInterestForm, PorchSignupForm
from .models				import Sponsor
from porchfestcore.models   import TempUpload
from pathlib                import Path
from django.core.files.base import ContentFile
from django.core.mail       import EmailMessage
from django.template.loader import render_to_string

def index(request):
    sponsors 		= Sponsor.objects.filter(is_active=True).order_by("level", "name")
    form		= PorchSignupForm()
    return render(request, 'website/front-page/index.html', {"sponsors": sponsors, 'form': form})

def porch_signup(request):
    temp_image = None
    if request.method == 'POST':
        form = PorchSignupForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get("temp_image_id") and not request.FILES.get("porch_picture"):
                temp_image = TempUpload.objects.filter(
                    id=request.POST["temp_image_id"]
                ).first()
                temp_file = temp_image.image
                filename = Path(temp_file.name).name
                instance.porch_picture.save(
                    filename,
                    ContentFile(temp_file.read()),
                    save=False
                )
                temp_image.delete()
            instance.save()
            html = render_to_string('website/emails/porch-signup-email.html', {
                'name': instance.owner_name,
            })
            email = EmailMessage(
                subject="New Porch Signup",
                body=html,
                from_email="info@towerporchfest.org",
                to=[instance.owner_email],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            return render(request, 'website/porch-signup-page/success.html')
        else:
            if "porch_picture" in request.FILES:
                temp_image = TempUpload.objects.create(
                    image=request.FILES["porch_picture"]
                )
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