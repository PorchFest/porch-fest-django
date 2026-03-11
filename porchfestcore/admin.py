import csv
from django.contrib 		    import admin
from django.contrib.gis.db 	    import models
from django.http		        import HttpResponse
from mapwidgets.widgets 	    import GoogleMapPointFieldWidget
from django.utils.translation   import gettext_lazy as _
from .models 				    import Performer, Porch, Request, Performance, TempUpload
from porchpanel.models          import Invitation
from .forms 				    import PerformanceForm, TimeInput

class PerformanceInline(admin.TabularInline):
    model 					= Performance
    form 					= PerformanceForm
    extra 					= 1
class InvitationInline(admin.TabularInline):
    model 					= Invitation
    extra 					= 1
class HasCoordinatesFilter(admin.SimpleListFilter):
    title = _("Coordinates")
    parameter_name  = "has_coordinates"

    def lookups(self, request, model_admin):
        return(
            ("yes", _("Has Coordinates")),
            ("no", _("No Coordinates")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(coordinates__isnull=False)
        if self.value() == "no":
            return queryset.filter(coordinates__isnull=True)
        return queryset

class HasInvitationFilter(admin.SimpleListFilter):
    title           = _("Invitation Status")
    parameter_name  = "invitation_status"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Has Invitation")),
            ("no", _("No Invitation")),
            ("accepted", _("Has Accepted Invitation")),
            ("not_accepted", _("Has Unaccepted Invitation")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(invitations__isnull=False).distinct()

        if self.value() == "no":
            return queryset.filter(invitations__isnull=True)

        if self.value() == "accepted":
            return queryset.filter(
                invitations__accepted=True
            ).distinct()

        if self.value() == "not_accepted":
            return queryset.filter(
                invitations__accepted=False
            ).distinct()

        return queryset

@admin.register(Porch)
class PorchAdmin(admin.ModelAdmin):
    list_display			= ('name', 'owner_name', 'owner_email', 'street_address', 'created_at',)
    search_fields 			= ('name', 'owner_name', 'owner_email', 'street_address',)
    list_filter 			= ('approved', 'created_at', HasCoordinatesFilter, HasInvitationFilter)
    formfield_overrides		= {
        models.PointField: {"widget": GoogleMapPointFieldWidget},
    }
    inlines 				= [PerformanceInline, InvitationInline]
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
