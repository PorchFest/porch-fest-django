from django.db import models

class Sponsor(models.Model):
    class SponsorLevel(models.TextChoices):
        PLATINUM 	= "platinum", 	"Platinum"
        GOLD 		= "gold", 		"Gold"
        SILVER 		= "silver", 	"Silver"
        BRONZE 		= "bronze", 	"Bronze"
        FRIEND 		= "friend", 	"Friend"

    name 			= models.CharField(max_length=200)
    website 		= models.URLField(blank=True)
    logo 			= models.ImageField(upload_to="sponsors/logos/")
    level 			= models.CharField(
        max_length=20,
        choices=SponsorLevel.choices,
        default=SponsorLevel.FRIEND,
    )
    description 	= models.TextField(blank=True)
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