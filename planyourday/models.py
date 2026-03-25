import uuid
from django.db import models

class Itinerary(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    performances    = models.ManyToManyField('porchfestcore.Performance', related_name='itineraries', blank=True)

    def ordered_performances(self):
        return self.performances.select_related(
            'performer',
            'porch'
        ).order_by('start_time')

    def __str__(self):
        return f"{self.id}"