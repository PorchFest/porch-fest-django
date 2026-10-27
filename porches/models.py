import								uuid
from django.db 						import models
from django.contrib.gis.db			import models as gis_models
from phonenumber_field.modelfields  import PhoneNumberField
from django.conf 					import settings
from django.contrib.auth.models		import User
from performers.models              import Performer, Genre
from django.utils.text              import slugify
from django.core.exceptions         import ValidationError
from django.template.loader         import render_to_string
from django.core.mail               import EmailMessage
from decouple                       import config
import os

class Porch(models.Model):
    class ContactMethod(models.TextChoices):
        EMAIL 			    = 'email', 'Email'
        PHONECALL 		    = 'phone', 'Phone Call'
        TEXTMESSAGE		    = 'text', 'Text Message'

    id 					    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				    = models.CharField(blank=True, max_length=255)
    user				    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    owner_name 		        = models.CharField(max_length=255)
    owner_email 		    = models.EmailField()
    owner_phone             = PhoneNumberField(null=True, blank=True)
    preferred_contact       = models.CharField(max_length=10, choices=ContactMethod.choices, default=ContactMethod.EMAIL)
    description 		    = models.TextField(blank=True)
    porch_picture		    = models.ImageField(upload_to='porches/', blank=True, null=True)
    vendor                  = models.BooleanField(default=False)
    childrens_activities    = models.BooleanField(default=False)
    number_of_performances  = models.IntegerField(default=1)
    after_party             = models.BooleanField(default=False)
    parking                 = models.BooleanField(default=False)
    info_booth              = models.BooleanField(default=False)
    porta_potty             = models.BooleanField(default=False)
    sponsored               = models.BooleanField(default=False)
    drinking_water          = models.BooleanField(default=False)
    bicycle_repair          = models.BooleanField(default=False)
    neighbors_hosting       = models.BooleanField(default=False)
    other_info 		        = models.TextField(blank=True)
    coordinates 		    = gis_models.PointField(blank=True, null=True, geography=True)
    street_address          = models.CharField(max_length=255)
    city                    = models.CharField(blank=True, max_length=100)
    state                   = models.CharField(blank=True, max_length=100)
    zip_code                = models.CharField(blank=True, max_length=20)
    country                 = models.CharField(blank=True, max_length=100)
    approved       		    = models.BooleanField(default=False)
    created_at              = models.DateTimeField(auto_now_add=True)
    original_created_at     = models.DateTimeField(null=True, blank=True)
    slug                    = models.SlugField(unique=True, blank=True, max_length=255)
    number                  = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Porch"
        verbose_name_plural = "Porches"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        is_approved = False
        if not self._state.adding:
            prev = Porch.objects.get(pk=self.pk)
            if not prev.approved and self.approved:
                is_approved = True

        super().save(*args, **kwargs)

        if config('DEBUG') == False:
            if is_approved:
                html = render_to_string('emails/porch-approved-email.html', {
                    'name': self.owner_name,
                })
                email = EmailMessage(
                    subject="Your Porch Has Been Approved! 🎉",
                    body=html,
                    from_email="Tower Porchfest <info@towerporchfest.org>",
                    to=[self.owner_email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

    def __str__(self):
        return self.name

class Performance(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    porch 				= models.ForeignKey(Porch, on_delete=models.CASCADE, related_name='performances')
    performer 			= models.ForeignKey(Performer, on_delete=models.CASCADE, related_name='performances')
    created_by 			= models.ForeignKey(User, on_delete=models.CASCADE, related_name='performances')
    start_time 			= models.TimeField()
    end_time 			= models.TimeField()
    created_at 			= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]
        
    def __str__(self):
        # conversion when using windows for local development
        time_format = '%#I:%M %p' if os.name == 'nt' else '%-I:%M %p'
        return f"{self.performer} at {self.porch} ({self.start_time.strftime(time_format)})"

class TempUpload(models.Model):
    image 		= models.ImageField(upload_to='temp_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)