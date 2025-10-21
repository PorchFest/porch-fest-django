from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from porchfestcore.models import Porch, Performance
from porchfestcore.forms import PerformanceFormDashboard
from .forms import PorchForm

def porch_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is a porch operator or superuser
            if user.is_superuser or user.groups.filter(name="Porch Operator").exists():
                login(request, user)
                return redirect("porchpanel:dashboard")
            else:
                messages.error(request, "You don’t have permission to access the Porch Panel.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "porchpanel/login.html")

def is_porch_operator(user):
    return user.groups.filter(name='Porch Operator').exists() or user.is_superuser

@login_required
def dashboard(request):
    porches = Porch.objects.filter(
        user=request.user,
    ).distinct()
    return render(request, 'porchpanel/dashboard.html', {'porches': porches})

@login_required
def porch_edit(request, pk):
    porch = get_object_or_404(
        Porch,
        Q(pk=pk),
        Q(user=request.user),
    )

    PerformanceFormSet = inlineformset_factory(
        parent_model=Porch,
        model=Performance,
        form=PerformanceFormDashboard,
        extra=1,
        can_delete=True
    )

    # PerformanceFormSet = inlineformset_factory(
    #     Performance,
    #     form=PerformanceFormDashboard,
    #     extra=1,
    #     can_delete=True
    # )
    performances_qs = Performance.objects.filter(porch=porch)

    # if request.method == "POST":
    #     porch_form = PorchForm(request.POST, instance=porch)
    #     formset = PerformanceFormSet(request.POST, instance=porch)

    #     if porch_form.is_valid() and formset.is_valid():
    #         porch_form.save()

    #         # Save performances and link them to the porch
    #         performances = formset.save(commit=False)
    #         for perf in performances:
    #             perf.porch = porch
    #             perf.created_by = request.user
    #             perf.save()
    #         for perf in formset.deleted_objects:
    #             perf.delete()

    #         return redirect("porchpanel:dashboard")
    #     else:
    #         print(f"porch: {porch_form.errors}")
    #         print(formset.errors)
    # else:
    #     porch_form = PorchForm(instance=porch)
    #     formset = PerformanceFormSet(queryset=performances_qs)
    if request.method == "POST":
        porch_form = PorchForm(request.POST, instance=porch)
        formset = PerformanceFormSet(request.POST, instance=porch)  # <-- bind to porch instance
        if porch_form.is_valid() and formset.is_valid():
            porch_form.save()
            formset.save()  # automatically sets porch FK
            return redirect("porchpanel:porch_list")
        else:
            print(f"porch: {porch_form.errors}")
            print(formset.errors)
    else:
        porch_form = PorchForm(instance=porch)
        formset = PerformanceFormSet(instance=porch)


    return render(
        request,
        "porchpanel/porch_edit.html",
        {
            "porch_form": porch_form,
            "formset": formset,
            "porch": porch,
        },
    )