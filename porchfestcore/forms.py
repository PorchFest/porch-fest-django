from django 	import forms
from .models 	import Porch

class PorchForm(forms.ModelForm):
    class Meta:
        model 	= Porch
        fields 	= ['name', 'owner_name', 'owner_email', 'street_address']
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        street_address = cleaned_data.get("street_address")
        email = cleaned_data.get("owner_email")
        if name and Porch.objects.filter(name__iexact=name).exists():
            self.add_error("name", "A porch with this name already exists.")
        if street_address and Porch.objects.filter(street_address__iexact=street_address).exists():
            self.add_error("street_address", "This address is already registered.")
        if email and Porch.objects.filter(owner_email__iexact=email).exists():
            self.add_error("owner_email", "This email has already been used.")
        return cleaned_data