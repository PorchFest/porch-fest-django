from django.contrib             import admin
from .models                    import Itinerary
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

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance_count')
    search_fields = ('id',)
    list_filter = ('created_at', HasPerformancesFilter,)

    def performance_count(self, obj):
        return obj.performances.count()

    performance_count.short_description = "Performances"