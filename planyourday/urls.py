from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.index, name='index'),
    path('performances/', views.PerformancesListView.as_view(), name='performances'),
]