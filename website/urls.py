from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pages/', views.pages, name='pages'),
	path('call-porches', views.call_for_porches, name='call-porches'),
    path('about/', views.about, name='about'),
]