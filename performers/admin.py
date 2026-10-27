from django.contrib import admin
from .models 				    import Performer, Genre
from porches.models import Performance, TempUpload
from django.utils.translation   import gettext_lazy as _

class HasPerformancesFilter(admin.SimpleListFilter):
    title = _("Performances")
    parameter_name  = "has_performances"

    def lookups(self, request, model_admin):
        return(
            ("yes", _("Has Performances")),
            ("no", _("No Performances")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(performances__isnull=False).distinct()
        if self.value() == "no":
            return queryset.filter(performances__isnull=True)
        return queryset

@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by',)
    search_fields = ['name']
    actions = ['export_as_csv',]
    list_filter = (HasPerformancesFilter,)
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="performers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name',])
        for obj in queryset:
            writer.writerow([
                obj.name,
            ])

        return response
    export_as_csv.short_description = "Export selected Performers to CSV"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass