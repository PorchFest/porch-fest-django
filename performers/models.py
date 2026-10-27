import                              uuid
from django.conf                    import settings
from django.contrib.auth.models     import User
from django.db                      import models
from phonenumber_field.modelfields  import PhoneNumberField

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)

        if Genre.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({
                "slug": "A genre with this slug already exists."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Performer(models.Model):
    id 					= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name 				= models.CharField(max_length=255)
    bio 				= models.TextField(blank=True)
    genres              = models.ManyToManyField(Genre, blank=True)
    member_count 		= models.IntegerField(default=1)
    instruments 		= models.IntegerField(default=0)
    link 				= models.URLField(blank=True)
    slug                = models.SlugField(unique=True, blank=True, max_length=255)
    profile_picture		= models.ImageField(upload_to='performers/', blank=True, null=True)
    email               = models.EmailField(null=True)
    phone_number        = PhoneNumberField(null=True, blank=True)
    user                = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_by 		    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performers', null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            i = 1
            while Performer.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name