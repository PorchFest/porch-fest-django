from django 	import forms
from .models 	import Porch

class PorchForm(forms.ModelForm):
	class Meta:
		model 	= Porch
		fields 	= ['name', 'owner_name', 'owner_email', 'street_address']