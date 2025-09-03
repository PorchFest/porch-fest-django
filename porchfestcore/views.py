from django.shortcuts 				import render
from django.views.generic 			import TemplateView
from django.http					import JsonResponse
from django.views.decorators.csrf	import csrf_exempt
from .forms							import PorchForm

def map_page(request):
    return render(request, 'porchfestcore/map.html')

def call_for_porches(request):
    if request.method == "POST":
        form = PorchForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Thanks for signing up!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})

    return JsonResponse({"success": False, "message": "Invalid request"})
