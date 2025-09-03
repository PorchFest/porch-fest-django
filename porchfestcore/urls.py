from django.urls	import path
from . 				import views

urlpatterns = [
	path('', views.map_page, name='map'),
	path('call-porches', views.call_for_porches, name='call-porches')
]