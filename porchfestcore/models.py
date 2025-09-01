import								uuid
from django.db 						import models
from django.contrib.gis.db			import models as gis_models
from django.conf 					import settings
from django.contrib.auth.models		import User

class Performer(models.Model):
    class Genre(models.TextChoices):
        ROCK 			= 'rock', 'Rock'
        JAZZ 			= 'jazz', 'Jazz'
        FOLK 			= 'folk', 'Folk'
        POP 			= 'pop', 'Pop'
        CLASSICAL		= 'classical', 'Classical'
        HIPHOP 			= 'hiphop', 'Hip Hop'
        OTHER 			= 'other', 'Other'

    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    bio 				= models.TextField(blank=True)
    genre				= models.CharField(max_length=20, choices=Genre.choices, default=Genre.OTHER)
    member_count 		= models.IntegerField(default=1)
    instruments 		= models.IntegerField(default=0)
    link 				= models.URLField(blank=True)
    # availability 		= models.JSONField()
    # location_pref		= models.TextField(blank=True)
    profile_picture		= models.ImageField(upload_to='performers/', blank=True, null=True)

    def __str__(self):
        return self.name

class Porch(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    user				= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performance_requests",
        blank=True,
        null=True,
    )
    owner_name 		    = models.CharField(max_length=255)
    owner_email 		= models.EmailField()
    description 		= models.TextField(blank=True)
    # capacity 			= models.IntegerField(default=0)
    # available_times 	= models.JSONField(default=list)
    coordinates 		= gis_models.PointField(blank=True, null=True, geography=True)
    street_address      = models.CharField(max_length=255)
    city                = models.CharField(blank=True, max_length=100)
    state               = models.CharField(blank=True, max_length=100)
    zip_code            = models.CharField(blank=True, max_length=20)
    country             = models.CharField(blank=True, max_length=100)
    approved       		= models.BooleanField(default=False)

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

    class Meta:
        ordering = ["start_time"]
        
    def __str__(self):
        return f"{self.performer} at {self.porch} ({self.start_time.strftime('%-I:%M %p')})"