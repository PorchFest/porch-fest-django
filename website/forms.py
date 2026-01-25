from django 					import forms
from django_recaptcha.fields	import ReCaptchaField
from django_recaptcha.widgets	import ReCaptchaV2Checkbox
from .models					import PorchInterest
from porchfestcore.models       import Porch

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

class PorchSignupForm(forms.ModelForm):
    # captcha		= ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model 	= Porch
        fields  = [
            'name',
            'street_address',
            'description',
            'owner_name',
            'owner_email',
            'owner_phone',
            'preferred_contact',
            'porch_picture',
            'vendor',
            'childrens_activities',
            'number_of_performances',
            'neighbors_hosting',
            'other_info',
            # 'captcha',
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': '1234 Street Ave'}),
            'number_of_performances': forms.NumberInput(attrs={'min': 1,'max': 15,}),
        }
    def __init__(self, *args, **kwargs):
        self.temp_image = kwargs.pop('temp_image', None)
        super().__init__(*args, **kwargs)

    def clean_porch_picture(self):
        porch_picture = self.cleaned_data.get("porch_picture")
        if not porch_picture and self.temp_image:
            return self.temp_image.image
        return porch_picture

    def clean(self):
        cleaned_data 	= super().clean()
        owner_name 		= cleaned_data.get("owner_name")
        street_address 	= cleaned_data.get("street_address")
        email 			= cleaned_data.get("owner_email")

        if street_address and Porch.objects.filter(street_address__iexact=street_address).exists():
            self.add_error("street_address", "This address is already registered.")

        if email and Porch.objects.filter(owner_email__iexact=email).exists():
            self.add_error("owner_email", "This email has already been used.")

        return cleaned_data