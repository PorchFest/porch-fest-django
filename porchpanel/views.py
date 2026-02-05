from django.contrib.auth.decorators import login_required
from django.shortcuts               import render, get_object_or_404, redirect
from django.forms                   import inlineformset_factory
from django.forms.models            import BaseInlineFormSet
from django.db.models               import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth            import authenticate, login
from django.contrib                 import messages
from django.contrib.auth.models     import Group, User
from porchfestcore.models           import Porch, Performance, Performer
from porchfestcore.forms            import PerformanceFormDashboard
from django.contrib.auth.forms      import UserCreationForm
from .forms                         import PorchForm, PerformerForm
from .models                        import Invitation

class PerformanceBaseFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        for form in self.forms:
            form.user = self.user

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

@login_required
def dashboard(request):
    if Porch.objects.filter(user=request.user).exists():
        has_porch = True
    porches = Porch.objects.filter(
        user=request.user,
    ).distinct()
    if Performer.objects.filter(created_by=request.user).exists():
        has_performer = True
    performers = Performer.objects.filter(created_by=request.user)
    return render(request, 'porchpanel/dashboard.html', {'porches': porches, 'has_porch': has_porch if 'has_porch' in locals() else False, 'performers': performers})

@login_required
def performer_edit(request, pk):
    performer = get_object_or_404(
        Performer,
        Q(pk=pk),
        Q(created_by=request.user),
    )
    if request.method == "POST":
        performer_form = PerformerForm(request.POST, instance=performer)
        if performer_form.is_valid():
            performer_form.save()
            messages.success(request, 'Performer details updated successfully')
            return redirect('porchpanel:performer_edit', performer.id)
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        performer_form = PerformerForm(instance=performer)
    return render(
        request,
        "porchpanel/performer_edit.html",
        {
            "performer_form": performer_form,
            "performer": performer,
        }
    )

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
        formset=PerformanceBaseFormSet,
        extra=1,
        can_delete=True
    )
    if request.method == "POST":
        if 'save_porch' in request.POST:
            porch_form = PorchForm(request.POST, instance=porch)
            if porch_form.is_valid():
                porch_form.save()
                porch_form = PorchForm(instance=porch)
                formset = PerformanceFormSet(instance=porch)
                return render(
                    request,
                    "porchpanel/porch_edit.html",
                    {
                        "porch_form": porch_form,
                        "formset": formset,
                        "porch": porch,
                    }
                )
            else:
                return render(
                    request,
                    "porchpanel/porch_edit.html",
                    {
                        "porch_form": porch_form,
                        "formset": formset,
                        "porch": porch,
                    }
                )
        elif 'save_performances' in request.POST:
            formset = PerformanceFormSet(request.POST, instance=porch, user=request.user)
            if formset.is_valid():
                performances = formset.save(commit=False)
                for performance in performances:
                    performance.porch = porch
                    performance.created_by = request.user
                    performance.save()
                for performance in formset.deleted_objects:
                    performance.delete()
                formset = PerformanceFormSet(instance=porch)
                return render(
                    request,
                    "porchpanel/components/performances_edit_form.html",
                    {
                        "formset": formset,
                        "porch": porch,
                    },
                )
            else:
                return render(
                    request,
                    "porchpanel/components/performances_edit_form.html",
                    {
                        "formset": formset,
                        "porch": porch,
                    },
                )
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