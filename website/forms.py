from django 					import forms
from django_recaptcha.fields	import ReCaptchaField
from django_recaptcha.widgets	import ReCaptchaV2Checkbox
from porchfestcore.models 		import Porch

class PorchForm(forms.ModelForm):
    captcha		= ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model 	= Porch
        fields 	= ['name', 'owner_name', 'owner_email', 'street_address', 'captcha']
        labels	= {
            'name': 'Porch Name',
            'street_address': 'Porch Address',
            'owner_name': 'Your Name',
            'owner_email': 'Your Email',
        }
        field_order	= ['name', 'street_address', 'owner_name', 'owner_email', 'captcha']
    
    def clean(self):
        cleaned_data 	= super().clean()
        name 			= cleaned_data.get("name")
        street_address 	= cleaned_data.get("street_address")
        email 			= cleaned_data.get("owner_email")
        if name and Porch.objects.filter(name__iexact=name).exists():
            self.add_error("name", "A porch with this name already exists.")

        if street_address and Porch.objects.filter(street_address__iexact=street_address).exists():
            self.add_error("street_address", "This address is already registered.")

        if email and Porch.objects.filter(owner_email__iexact=email).exists():
            self.add_error("owner_email", "This email has already been used.")

        return cleaned_data