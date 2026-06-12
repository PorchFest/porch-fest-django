from django 					import forms
from django_recaptcha.fields	import ReCaptchaField
from django_recaptcha.widgets	import ReCaptchaV2Checkbox
from .models					import PorchInterest
from src.apps.porchpanel.models import Invitation
from src.apps.porchfestcore.models       import Porch, Performer

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
    captcha		= ReCaptchaField(widget=ReCaptchaV2Checkbox)
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
            'captcha',
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
        
class PerformerSignupForm(forms.ModelForm):
    performer = forms.ModelChoiceField(
        queryset=Performer.objects.all(),
        required=False,
        widget=forms.HiddenInput(),
    )

    # captcha		= ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model 	= Performer
        fields  = [
            'name',
            'email',
            'phone_number',
            'bio',
            'genres',
            'member_count',
            'instruments',
            'link',
            # 'captcha',
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]

        if Invitation.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An invitation has already been sent to this email."
            )

        return email
    
    def clean(self):
        cleaned_data 	= super().clean()
        name            = cleaned_data.get('name')
        email 			= cleaned_data.get('email')
        # performer       = cleaned_data.get('performer')

        performer       = cleaned_data.get('performer')
        if not performer and Performer.objects.filter(name__iexact=name).exists():
            performer   = Performer.objects.get(name__iexact=name)
        if performer and performer.user:
            self.add_error(
                "performer",
                "This performer has already been claimed."
            )
        if performer:
            if Invitation.objects.filter(performer=performer).exists():
                self.add_error(
                    "performer",
                    "This performer already has an invitation. Although it will expire in two weeks so maybe try again or email us with your demands"
                )

        if email and Performer.objects.filter(email__iexact=email).exists():
            self.add_error("email", "This email has already been used.")

        return cleaned_data
    
    def get_or_create_performer(self):
        selected = self.cleaned_data.get("performer")
        if selected:
            return selected
        return super().save()

        selected = self.cleaned_data.get("performer")
        if selected:
            return selected
        return Performer.objects.create(
            name=self.cleaned_data["name"],
            email=self.cleaned_data.get("email"),
        )