from django.contrib.auth.decorators import login_required
from django.shortcuts               import render, get_object_or_404, redirect
from django.forms                   import inlineformset_factory
from django.db.models               import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth            import authenticate, login
from django.contrib                 import messages
from django.contrib.auth.models     import Group, User
from porchfestcore.models           import Porch, Performance
from porchfestcore.forms            import PerformanceFormDashboard
from django.contrib.auth.forms      import UserCreationForm
from .forms                         import PorchForm
from .models                        import Invitation

def accept_invite(request, token):
    invitation = get_object_or_404(Invitation, token=token)

    if not invitation.is_valid():
        return render(request, "porchpanel/invite_invalid.html")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user                = form.save(commit=False)
            user.email          = invitation.owner_email
            user.save()
            invitation.accepted = True
            invitation.save()
            login(request, user)
            return redirect("porchpanel:dashboard")
    else:
        form = UserCreationForm()

    return render(request, "porchpanel/accept_invite.html", {"form": form, "email": invitation.owner_email})


def porch_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser or user.groups.filter(name="Porch Host").exists():
                login(request, user)
                return redirect("porchpanel:dashboard")
            else:
                messages.error(request, "You don’t have permission to access the Porch Panel.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "porchpanel/login.html")

# def is_porch_operator(user):
#     return user.groups.filter(name='Porch Operator').exists() or user.is_superuser

@login_required
def dashboard(request):
    if Porch.objects.filter(user=request.user).exists():
        has_porch = True
    porches = Porch.objects.filter(
        user=request.user,
    ).distinct()
    return render(request, 'porchpanel/dashboard.html', {'porches': porches, 'has_porch': has_porch if 'has_porch' in locals() else False})

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
    if request.method == "POST":
        porch_form = PorchForm(request.POST, instance=porch)
        formset = PerformanceFormSet(request.POST, instance=porch)
        if porch_form.is_valid() and formset.is_valid():
            porch_form.save()
            performances = formset.save(commit=False)
            for perf in performances:
                perf.porch = porch
                perf.created_by = request.user
                perf.save()
            for perf in formset.deleted_objects:
                perf.delete()
            porch_form = PorchForm(instance=porch)
            formset = PerformanceFormSet(instance=porch)
            return render(request, "porchpanel/components/porch_edit_form.html", {
                "porch_form": porch_form,
                "formset": formset,
                "porch": porch,
                "saved": True,
            })
        else:
            print(porch_form.errors, formset.errors)
            return render(request, "porchpanel/components/porch_edit_form.html", {
                "porch_form": porch_form,
                "formset": formset,
                "porch": porch,
            })
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

@login_required
def create_porch(request):
    if Porch.objects.filter(user=request.user).exists():
        return redirect('porchpanel:porch_edit', Porch.objects.get(user=request.user).id)
    if request.method == 'POST':
        form 				= PorchForm(request.POST)
        if form.is_valid():
            porch 			= form.save(commit=False)
            porch.user		= request.user
            porch.save()
            messages.success(request, 'Your porch has been created')
            return redirect('porchpanel:porch_edit', porch.id)
    else:
        form 				= PorchForm()
    return render(request, 'porchpanel/create_porch.html', {'form': form})