from django.contrib 		import admin
from django.contrib.gis.db 	import models
import csv
from django.http		    import HttpResponse
from mapwidgets.widgets 	import GoogleMapPointFieldWidget
from .models 				import Performer, Porch, Request, Performance, TempUpload
from .forms 				import PerformanceForm, TimeInput

class PerformanceInline(admin.TabularInline):
    model 					= Performance
    form 					= PerformanceForm
    extra 					= 1

@admin.register(Porch)
class PorchAdmin(admin.ModelAdmin):
    list_display			= ('name', 'owner_name', 'owner_email', 'street_address', 'created_at',)
    search_fields 			= ('name', 'city', 'state', 'zip_code', 'country')
    list_filter 			= ('approved', 'created_at')
    formfield_overrides		= {
        models.PointField: {"widget": GoogleMapPointFieldWidget},
    }
    inlines 				= [PerformanceInline]
    ordering				= ('-created_at',)
    actions                 = ['export_as_csv', 'approve_porches']

    class Media:
        js 					= ('porchfestcore/js/porch-admin.js',)
    def approve_porches(self, request, queryset):
        queryset.update(approved=True)
    approve_porches.short_description = "Approve selected porches"
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="porches.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Preferred Contact', 'Address', 'Porch Name', 'Description', 'Number of Performances', 'Vendor', 'Children\'s Activities', 'Neighbors Hosting', 'Other Info'])

        for obj in queryset:
            writer.writerow([
                obj.owner_name,
                obj.owner_email,
                obj.owner_phone,
                obj.preferred_contact,
                obj.street_address,
                obj.name,
                obj.description,
                obj.number_of_performances,
                obj.vendor,
                obj.childrens_activities,
                obj.neighbors_hosting,
                obj.other_info,
            ])

        return response
    export_as_csv.short_description = "Export selected Porch to CSV"
  
@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput},
    }

@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by',)
    # search_fields = ('name', 'genre')
    # list_filter = ('genre', 'created_at')
    # ordering = ('-created_at',)
admin.site.register(Request)
admin.site.register(TempUpload)
