from django.db              import models
from porchfestcore.models   import Porch

class Sponsor(models.Model):
    class SponsorLevel(models.TextChoices):
        EVENT 	    = "event",      "Event"
        DIAMOND     = "diamond",    "Diamond"
        PLATINUM    = "platinum", 	"Platinum"
        GOLD 		= "gold", 	    "Gold"
        COMMUNITY   = "community",  "Community"

    name 			= models.CharField(max_length=200)
    website 		= models.URLField(blank=True)
    logo 			= models.ImageField(upload_to="sponsors/logos/")
    map_icon        = models.ImageField(blank=True, upload_to="sponsors/map_icons")
    level 			= models.CharField(
        max_length=20,
        choices=SponsorLevel.choices,
        default=SponsorLevel.COMMUNITY,
    )
    description 	= models.TextField(blank=True)
    porch = models.OneToOneField(
        Porch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sponsor'
    )
    is_active 		= models.BooleanField(default=True)
    created_at 		= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering 	= ["level", "name"]

    def __str__(self):
        return f"{self.name} ({self.level})"

class PorchInterest(models.Model):
	owner_name		= models.CharField(max_length=255)
	owner_email		= models.EmailField()
	street_address	= models.CharField(max_length=255)

	def __str__(self):
		return f"{self.owner_name}, {self.owner_email}"