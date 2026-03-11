from django.urls    import path
from .              import endpoints

urlpatterns = [
    path('porches', endpoints.Porches.as_view(), name='porches'),
]