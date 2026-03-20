from django.urls	import path
from . 				import views

urlpatterns = [
    path('', views.index, name='index'),
    path('performances', views.PerformancesListView.as_view(), name='performances'),
    path('add-performance', views.add_performance, name='add_performance'),
    path('remove-performance', views.remove_performance, name='remove_performance'),
]