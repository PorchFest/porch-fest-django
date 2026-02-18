from django     import forms
from .models    import Performance, Performer

class TimeInput(forms.TimeInput):
	input_type 				= "time"

class PerformanceForm(forms.ModelForm):
	class Meta:
		model 				= Performance
		fields 				= '__all__'
		widgets 			= {
			'start_time': 	TimeInput(),
			'end_time': 	TimeInput(),
		}