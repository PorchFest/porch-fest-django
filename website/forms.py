from django 					import forms
from django_recaptcha.fields	import ReCaptchaField
from django_recaptcha.widgets	import ReCaptchaV2Checkbox
from .models					import PorchInterest

class PorchInterestForm(forms.ModelForm):
    captcha		= ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model 	= PorchInterest
        fields 	= ['owner_name', 'owner_email', 'street_address', 'captcha',]
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': '1234 Street Ave'}),
        }
    
    def clean(self):
        cleaned_data 	= super().clean()
        owner_name 		= cleaned_data.get("owner_name")
        street_address 	= cleaned_data.get("street_address")
        email 			= cleaned_data.get("owner_email")

        if street_address and PorchInterest.objects.filter(street_address__iexact=street_address).exists():
            self.add_error("street_address", "This address is already registered.")

        if email and PorchInterest.objects.filter(owner_email__iexact=email).exists():
            self.add_error("owner_email", "This email has already been used.")

        return cleaned_data