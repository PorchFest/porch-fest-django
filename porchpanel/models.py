import uuid
from django.conf    import settings
from django.db      import models
from django.utils   import timezone
from django.urls    import reverse
from datetime       import timedelta

def default_expiration():
    return timezone.now() + timedelta(days=7)

class Invitation(models.Model):
    owner_email = models.EmailField(unique=True)
    token       = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    expires_at  = models.DateTimeField(default=default_expiration)
    accepted    = models.BooleanField(default=False)

    def is_valid(self):
        return not self.accepted and timezone.now() < self.expires_at
    
    def invite_url(self, request=None):
        path = reverse("porchpanel:accept_invite", args=[self.token])
        base_url = settings.BASE_URL
        path = f"{base_url}{path}"
        if request:
            return request.build_absolute_uri(path)
        return path

    def __str__(self):
        return self.owner_email
