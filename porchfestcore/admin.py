from django.contrib 		import admin
from django.contrib.gis.db 	import models
from mapwidgets.widgets 	import GoogleMapPointFieldWidget
from .models 				import Performer, Porch, Request, Performance
from .forms 				import PerformanceForm, TimeInput

class PerformanceInline(admin.TabularInline):
    model 					= Performance
    form 					= PerformanceForm
    extra 					= 1

@admin.register(Porch)
class PorchAdmin(admin.ModelAdmin):
	list_display			= ('name', 'owner_name', 'owner_email', 'street_address', 'original_created_at',)
	fields 					= ('name', 'approved', 'owner_name', 'user', 'owner_email', 'coordinates', 'description', 'street_address', 'city', 'state', 'zip_code', 'country',)
	search_fields 			= ('name', 'city', 'state', 'zip_code', 'country')
	list_filter 			= ('approved',)
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
