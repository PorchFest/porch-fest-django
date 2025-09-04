from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pages/', views.pages, name='pages'),
	path('porch-list-signup', views.porch_list_signup, name='porch-list-signup'),
    path('about/', views.about, name='about'),
]