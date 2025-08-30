from django.urls	import path
from . 				import views

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('map/', views.map_page, name='map'),
	path('pages/', views.pages, name='pages'),
	path('call-porches/', views.call_porches, name='call-porches'),
]