from django.urls	import path
from . 				import views

urlpatterns = [
	path('', views.coming_soon, name='map'),
	path('obscure-map', views.map_page, name='obscure_map'),
	path('marker-map', views.bland_map, name='marker_map'),
]