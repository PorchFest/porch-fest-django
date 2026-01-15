from django.contrib 	import admin
from .models			import Sponsor, PorchInterest
from django.http		import HttpResponse
import csv

@admin.register(PorchInterest)
class PorchInterestAdmin(admin.ModelAdmin):
    actions         = ['export_as_csv']
    list_display    = ('id', 'owner_name', 'owner_email', 'street_address',)

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="porch_interests.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Address'])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.owner_name,
                obj.owner_email,
                obj.street_address,
            ])

        return response
    export_as_csv.short_description = "Export selected Porch Interests to CSV"

admin.site.register(Sponsor)