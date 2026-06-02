from django.contrib 			import admin
from django.urls 				import path, include
from django.conf 				import settings
from django.conf.urls.static	import static
from django.contrib.auth        import views as auth_views
admin.site.site_header 			= 'Tower Porchfest Admin'
admin.site.index_title			= 'Admin'
admin.site.site_title			= 'Porchfest'

urlpatterns = [
	path('', include('src.apps.website.urls')),
    path('map/', include('src.apps.porchfestcore.urls')),
    path('plan-your-day/', include('src.apps.planyourday.urls')),
    path('dashboard/', include('src.apps.porchpanel.urls')),
    path('porchfestpeeps/', admin.site.urls),
    path('api/porches/', include('src.apps.porchfestcore.api.urls')),
    path('api/plan-your-day/', include('src.apps.planyourday.api.urls')),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)