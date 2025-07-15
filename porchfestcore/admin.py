from django.contrib import admin
from .models import Performer, Porch, Request, Performance

# Register your models here.

admin.site.register(Performer)
admin.site.register(Porch)
admin.site.register(Request)
admin.site.register(Performance)