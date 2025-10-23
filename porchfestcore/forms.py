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

class PerformanceFormDashboard(forms.ModelForm):
    new_performer_name = forms.CharField(required=False, label="New Performer")
    performer = forms.ModelChoiceField(
        queryset=Performer.objects.all(),
        required=False
    )

    class Meta:
        model = Performance
        fields = ['performer', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        performer = cleaned_data.get('performer')
        new_name = cleaned_data.get('new_performer_name')

        if not performer and not new_name:
            raise forms.ValidationError(
                "You must select an existing performer or enter a new one."
            )
        if performer and new_name:
            raise forms.ValidationError(
                "Please either select an existing performer or enter a new one, not both."
            )
        return cleaned_data

    def save(self, commit=True):
        performer = self.cleaned_data.get('performer')
        new_name = self.cleaned_data.get('new_performer_name')
        if not performer and new_name:
            performer, _ = Performer.objects.get_or_create(name=new_name)
        self.instance.performer = performer
        return super().save(commit=commit)
