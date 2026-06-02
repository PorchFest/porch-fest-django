from django.urls    import path
from .              import endpoints

urlpatterns = [
    path('performances', endpoints.Performances.as_view(), name='performances-api'),
    # path('itinerary/create', endpoints.create_itinerary, name='create_itinerary'),
    # path('itinerary/<str:itinerary_id>', endpoints.get_itinerary, name='get_itinerary'),
    # path('itinerary/add/', endpoints.add_performance, name='add_performance'),
    # path('itinerary/<str:itinerary_id>/remove', endpoints.remove_performance, name='remove_performance'),
]