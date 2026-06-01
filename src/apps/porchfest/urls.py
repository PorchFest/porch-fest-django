from django.urls	import path
from . 				import views

urlpatterns = [
	path('', views.map_page, name='map'),
	# path('obscure-map', views.map_page, name='obscure_map'),
	# path('marker-map', views.bland_map, name='marker_map'),
]

# urlpatterns = [
#     path('', views.plan_your_day, name='plan_your_day'),
#     path('<uuid:itinerary_id>', views.plan_your_day, name='shared_itinerary'),
#     path('performances/', views.PerformancesListView.as_view(), name='performances'),
#     path('performances/<uuid:itinerary_id>', views.PerformancesListView.as_view(), name='performances'),
#     path('add-performance/', views.add_performance, name='add_performance'),
#     path('add-performance/<uuid:itinerary_id>/', views.add_performance, name='add_performance_shared'),
#     path('remove-performance/', views.remove_performance, name='remove_performance'),
#     path('remove-performance/<uuid:itinerary_id>/', views.remove_performance, name='remove_performance_shared'),
# ]