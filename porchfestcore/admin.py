from django.contrib 		import admin
from django.contrib.gis.db 	import models
from mapwidgets.widgets 	import GoogleMapPointFieldWidget
from django 				import forms
from .models 				import Performer, Porch, Request, Performance

# Use HTML5 time input for start and end times
# ********************************************
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

class PerformanceInline(admin.TabularInline):
    model 					= Performance
    form 					= PerformanceForm
    extra 					= 1
# ********************************************
# ********************************************

@admin.register(Porch)
class VenueAdmin(admin.ModelAdmin):
	list_display			= ('name', 'street_address', 'description')
	fields 					= ('name', 'owner', 'coordinates', 'description', 'street_address', 'city', 'state', 'zip_code', 'country')
	search_fields 			= ('name', 'city', 'state', 'zip_code', 'country')
	list_filter 			= ('state', 'country')
	formfield_overrides		= {
        models.PointField: {"widget": GoogleMapPointFieldWidget},
    }
	inlines 				= [PerformanceInline]

	class Media:
		js 					= ('porchfestcore/js/porch-admin.js',)
  
@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    formfield_overrides = {
		models.TimeField: {'widget': TimeInput},
	}

admin.site.register(Performer)
admin.site.register(Request)
