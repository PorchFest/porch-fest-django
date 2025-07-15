import 		uuid
from 		django.db import models
from 		django.contrib.auth.models import User

class Performer(models.Model):
    GENRE_CHOICES = [
        ('rock', 		'Rock'),
        ('jazz', 		'Jazz'),
        ('folk', 		'Folk'),
        ('pop', 		'Pop'),
        ('classical',	'Classical'),
        ('hiphop', 		'Hip Hop'),
        ('other', 		'Other'),
    ]

    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    genre				= models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    bio 				= models.TextField(blank=True)
    instruments 		= models.TextField(blank=True)
    availability 		= models.JSONField(default=list)  # Later could be DateTime ranges
    location_pref		= models.TextField(blank=True)
    profile_picture		 = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Porch(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    owner_name 			= models.CharField(max_length=255)
    address 			= models.CharField(max_length=255)
    lat 				= models.FloatField(null=True, blank=True)
    lng 				= models.FloatField(null=True, blank=True)
    description 		= models.TextField(blank=True)
    capacity 			= models.IntegerField(default=0)
    available_times 	= models.JSONField(default=list)

    def __str__(self):
        return self.name

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

class Performance(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    porch 				= models.ForeignKey(Porch, on_delete=models.CASCADE, related_name='performances')
    performer 			= models.ForeignKey(Performer, on_delete=models.CASCADE)
    created_by 			= models.ForeignKey(User, on_delete=models.CASCADE, related_name='performances')
    start_time 			= models.TimeField()
    end_time 			= models.TimeField()
    created_at 			= models.DateTimeField(auto_now_add=True)
