import uuid
from django.conf    import settings
from django.db      import models
from django.utils   import timezone
from django.urls    import reverse
from datetime       import timedelta
from porches.models import Porch
from performers.models import Performer
from django.contrib.auth.models import User


def default_expiration():
    return timezone.now() + timedelta(days=7)

class Invitation(models.Model):
    email = models.EmailField(unique=True)
    porch       = models.ForeignKey('porchfestcore.Porch', on_delete=models.CASCADE, related_name='invitations', null=True, blank=True)
    performer   = models.ForeignKey('performers.Performer', on_delete=models.CASCADE, related_name='invitations', null=True, blank=True)
    token       = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(default=default_expiration)
    accepted    = models.BooleanField(default=False)

    def is_valid(self):
        return not self.accepted and timezone.now() < self.expires_at
    
    def invite_url(self, request=None):
        path = reverse("dashboard:accept_invite", args=[self.token])
        base_url = settings.BASE_URL
        path = f"{base_url}{path}"
        if request:
            return request.build_absolute_uri(path)
        return path

    def __str__(self):
        return self.email


class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 	'Pending'),
        ('accepted', 	'Accepted'),
        ('declined', 	'Declined'),
        ('expired', 	'Expired'),
    ]

    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    porch 				= models.ForeignKey(Porch, on_delete=models.CASCADE)
    performer 			= models.ForeignKey(Performer, on_delete=models.CASCADE)
    requested_by 		= models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    start_time 			= models.TimeField()
    end_time 			= models.TimeField()
    status 				= models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at 			= models.DateTimeField(auto_now_add=True)
    responded_at 		= models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.performer.name} at {self.porch.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        is_accepting = False

        if not self._state.adding:
            prev = Request.objects.get(pk=self.pk)
            if prev.status != 'accepted' and self.status == 'accepted':
                is_accepting = True

        super().save(*args, **kwargs)

        if is_accepting:
            Performance.objects.create(
                porch=self.porch,
                performer=self.performer,
                created_by=self.requested_by,
                start_time=self.start_time,
                end_time=self.end_time
            )