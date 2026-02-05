from django                 import forms
from porchfestcore.models   import Porch, Performer
from mapwidgets.widgets 	import GoogleMapPointFieldWidget

class PorchForm(forms.ModelForm):
    class Meta:
        model = Porch
        fields  = ('name', 'owner_name', 'coordinates', 'description', 'porch_picture', 'vendor', 'childrens_activities', 'street_address', 'city', 'state', 'zip_code', 'country',)
        widgets = {
            'coordinates': GoogleMapPointFieldWidget,
            'street_address': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'zip_code': forms.HiddenInput(),
            'country': forms.HiddenInput(),
        }
        labels = {
            'street_address': '',
            'city': '',
            'state': '',
            'zip_code': '',
            'country': '',
        }

class PerformerForm(forms.ModelForm):
    class Meta:
        model = Performer
        fields = ('name', 'bio', 'genre', 'member_count', 'instruments', 'link', 'profile_picture',)