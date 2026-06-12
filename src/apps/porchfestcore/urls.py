from django.urls	import path
from . 				import views

urlpatterns = [
	path('', views.map_page, name='map'),
	path('performer-search/', views.PerformerListView.as_view(), name='performer-search')
	# path('obscure-map', views.map_page, name='obscure_map'),
	# path('marker-map', views.bland_map, name='marker_map'),
]