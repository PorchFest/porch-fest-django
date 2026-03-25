from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.plan_your_day, name='plan-your-day'),
    path('<uuid:itinerary_id>', views.plan_your_day, name='shared_itinerary'),
    path('performances/', views.PerformancesListView.as_view(), name='performances'),
    path('add-performance/<uuid:itinerary_id>/', views.add_performance, name='add_performance'),
    path('remove-performance/<uuid:itinerary_id>/', views.remove_performance, name='remove_performance'),
]