from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.index, name='index'),
	path('porch-list-signup', views.porch_list_signup, name='porch-list-signup'),
    path('about/', views.about, name='about'),
]