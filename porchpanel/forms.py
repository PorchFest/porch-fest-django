from django                 import forms
from porchfestcore.models   import Porch
from mapwidgets.widgets 	import GoogleMapPointFieldWidget

class PorchForm(forms.ModelForm):
    class Meta:
        model = Porch
        fields  = ('name', 'owner_name', 'coordinates', 'description', 'street_address', 'city', 'state', 'zip_code', 'country',)
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