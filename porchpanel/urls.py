from django.urls	        import path
from . 				        import views
from django.contrib.auth    import views as auth_views

app_name = "porchpanel"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("login/", views.porch_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="porchpanel:login"), name="logout"),
    path('porches/<uuid:pk>/edit/', views.porch_edit, name='porch_edit'),
    path("porches/create/", views.create_porch, name="create_porch"),
]