import 		uuid
from 		django.db import models

class Performer(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    genre 				= models.CharField(max_length=255)
    instruments 		= models.TextField(blank=True)
    availability 		= models.JSONField(default=list)  # Later could be DateTime ranges
    location_pref		= models.TextField(blank=True)
    profile_picture		 = models.URLField(blank=True)
    bio 				= models.TextField(blank=True)

    def __str__(self):
        return self.name

class Porch(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_name 			= models.CharField(max_length=255)
    address 			= models.CharField(max_length=255)
    lat 				= models.FloatField(null=True, blank=True)
    lng 				= models.FloatField(null=True, blank=True)
    description 		= models.TextField(blank=True)
    capacity 			= models.IntegerField(default=0)
    available_times 	= models.JSONField(default=list)
    finalized 			 = models.BooleanField(default=False)

    def __str__(self):
        return self.address

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
    status 				= models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at 			= models.DateTimeField(auto_now_add=True)
    responded_at 		= models.DateTimeField(null=True, blank=True)

class Performance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    porch 				= models.ForeignKey(Porch, on_delete=models.CASCADE)
    performer 			= models.ForeignKey(Performer, on_delete=models.CASCADE)
    scheduled_time 		= models.DateTimeField()
    start_time 			= models.TimeField()
    end_time 			= models.TimeField()
    status 				= models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at 			= models.DateTimeField(auto_now_add=True)
