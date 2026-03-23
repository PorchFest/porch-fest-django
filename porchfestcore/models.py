import								uuid
from django.db 						import models
from django.contrib.gis.db			import models as gis_models
from phonenumber_field.modelfields  import PhoneNumberField
from django.conf 					import settings
from django.contrib.auth.models		import User
from django.utils.text              import slugify
from django.template.loader         import render_to_string
from django.core.mail               import EmailMessage

class Performer(models.Model):
    class Genre(models.TextChoices):
        AERIALIST             = 'aerialist', 'Aerialist'
        ACOUSTIC              = 'acoustic', 'Acoustic'
        ALTERNATIVE           = 'alternative', 'Alternative'
        AMERICANA             = 'americana', 'Americana'
        BELLYDANCE            = 'bellydance', 'Bellydance'
        BLUEGRASS             = 'bluegrass', 'Bluegrass'
        BLUES                 = 'blues', 'Blues'
        CAJUN                 = 'cajun', 'Cajun'
        CLASSICAL             = 'classical', 'Classical'
        CLASSIC_ROCK          = 'classic_rock', 'Classic Rock'
        COMEDY                = 'comedy', 'Comedy'
        CONTEMPORARY          = 'contemporary', 'Contemporary'
        COUNTRY               = 'country', 'Country'
        DANCE_ELECTRONIC      = 'dance_electronic', 'Dance / Electronic / House'
        DARK_JAZZ             = 'dark_jazz', 'Dark Jazz'
        DJ                    = 'dj', 'DJ'
        DRAG                  = 'drag', 'Drag'
        DRUMMING              = 'drumming', 'Drumming'
        DUBSTEP               = 'dubstep', 'Dubstep'
        ECLECTIC              = 'eclectic', 'Eclectic'
        ELECTRONIC            = 'electronic', 'Electronic'
        FLAMENCO              = 'flamenco', 'Flamenco'
        FOLK                  = 'folk', 'Folk'
        FUNK                  = 'funk', 'Funk'
        HARDCORE              = 'hardcore', 'Hardcore'
        HIP_HOP_RAP           = 'hip_hop_rap', 'Hip-Hop / Rap'
        HOUSE                 = 'house', 'House'
        INDIE                 = 'indie', 'Indie'
        JAZZ                  = 'jazz', 'Jazz'
        LATIN                 = 'latin', 'Latin'
        MARIACHI              = 'mariachi', 'Mariachi'
        MEDICINE_DRUM         = 'medicine_drum', 'Medicine Drum'
        METAL                 = 'metal', 'Metal'
        PAINTER               = 'painter', 'Painter'
        PIANO                 = 'piano', 'Piano'
        POETRY_SPOKEN_WORD    = 'poetry_spoken_word', 'Poetry / Spoken Word'
        POP                   = 'pop', 'Pop'
        POST_HUMAN_ROCK       = 'post_human_rock', 'Post Human Civilization Rock'
        PROG_ROCK             = 'prog_rock', 'Prog Rock'
        PSYCHEDELIC_ROCK      = 'psychedelic_rock', 'Psychedelic Rock'
        PUNK                  = 'punk', 'Punk'
        RNB                   = 'rnb', 'R & B'
        REGGAE                = 'reggae', 'Reggae'
        ROCK                  = 'rock', 'Rock'
        ROCK_AND_ROLL         = 'rock_and_roll', 'Rock and Roll'
        ROCKABILLY            = 'rockabilly', 'Rockabilly'
        SHOEGAZE              = 'shoegaze', 'Shoegaze'
        SKA                   = 'ska', 'Ska'
        SALSA_CUMBIA          = 'salsa_cumbia', 'Salsa / Cumbia'
        SOUL_BLUES            = 'soul_blues', 'Soul / Blues'
        SOUND_BATH            = 'sound_bath', 'Sound Bath Practitioner'
        SINGER_SONGWRITER     = 'singer_songwriter', 'Singer Songwriter'
        SWING                 = 'swing', 'Swing'
        TECH_HOUSE            = 'tech_house', 'Tech House'
        TECHNO                = 'techno', 'Techno'
        THRASH_METAL          = 'thrash_metal', 'Thrash Metal'
        TRAP                  = 'trap', 'Trap'
        TRIP_HOP              = 'trip_hop', 'Trip Hop'
        VOCALS                = 'vocals', 'Vocals'
        YOGA                  = 'yoga', 'Yoga'
        ZYDECO                = 'zydeco', 'Zydeco'
        OTHER                 = 'other', 'Other'

    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    bio 				= models.TextField(blank=True)
    genre				= models.CharField(max_length=20, choices=Genre.choices, default=Genre.OTHER)
    member_count 		= models.IntegerField(default=1)
    instruments 		= models.IntegerField(default=0)
    link 				= models.URLField(blank=True)
    profile_picture		= models.ImageField(upload_to='performers/', blank=True, null=True)
    created_by 		    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performers')

    def __str__(self):
        return self.name

class Porch(models.Model):
    class ContactMethod(models.TextChoices):
        EMAIL 			= 'email', 'Email'
        PHONECALL 		= 'phone', 'Phone Call'
        TEXTMESSAGE		= 'text', 'Text Message'

    id 					    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				    = models.CharField(blank=True, max_length=255)
    user				    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performance_requests",
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        is_approved = False
        if not self._state.adding:
            prev = Porch.objects.get(pk=self.pk)
            if not prev.approved and self.approved:
                is_approved = True

        super().save(*args, **kwargs)

        if is_approved:
            html = render_to_string('website/emails/porch-approved-email.html', {
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

class TempUpload(models.Model):
    image 		= models.ImageField(upload_to='temp_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)