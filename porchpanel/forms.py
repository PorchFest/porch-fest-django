from django                 import forms
from porchfestcore.models   import Porch, Performer, Performance
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
            'start_time': forms.TimeInput(attrs={'type': 'time', 'min': '10:00'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'max': '19:00'}),
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
            performer, _ = Performer.objects.get_or_create(name=new_name, created_by=self.user)
        self.instance.performer = performer
        return super().save(commit=commit)
