from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.index, name='index'),
	path('porch-list-signup', views.porch_list_signup, name='porch-list-signup'),
    path('about/', views.about, name='about'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('sponsorship/', views.sponsorship, name='sponsorship'),
    path('donate/', views.donate, name='donate'),
    path('porch-signup/', views.porch_signup, name='porch-signup'),
    path('porches/<slug:slug>/', views.porch_page, name='porch_page'),
]