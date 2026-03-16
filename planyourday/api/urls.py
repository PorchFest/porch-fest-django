from django.urls    import path
from .              import endpoints

urlpatterns = [
    path('performances', endpoints.Performances.as_view(), name='performances'),
]