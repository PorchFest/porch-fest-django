from django import forms
from porchfestcore.models import Porch

class PorchForm(forms.ModelForm):
    class Meta:
        model = Porch
        fields = ['name', 'street_address']
