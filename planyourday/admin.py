from django.contrib     import admin
from .models            import Itinerary

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'performance_count')

    def performance_count(self, obj):
        return obj.performances.count()

    performance_count.short_description = "Performances"