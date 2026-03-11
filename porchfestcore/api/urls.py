from django.urls    import path
from .              import endpoints

urlpatterns = [
    path('porch-map', endpoints.PorchMap.as_view(), name='porch-map'),
]