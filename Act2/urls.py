from django.contrib import admin
from django.urls import path, include
from dashboard.views import (
    dashboard_view, reports_view, settings_view,
    portfolio_view, crud_test_view, delete_entry_view, rate_limit
)
from ua.views import login_page, signup_page, classic_login
from .views import admin_dashboard_view
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import upload_profile
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminpanel/', include('adminpanel.urls')),
     path('', include('ua.urls')),

    path('', login_page, name='home'),
    path('signup/', signup_page, name='signup'),

    path('dashboard/', dashboard_view, name='dashboard'),
    path('reports/', reports_view, name='reports'),
    path('settings/', settings_view, name='settings'),
    path('portfolio/', portfolio_view, name='portfolio'),

    path('portfolio/crud/', crud_test_view, name='crud_test'),
    path('crud-test/delete/<int:entry_id>/', delete_entry_view, name='delete_entry'),

    path('auth/classic-login/', classic_login, name='classic_login'),
    path('login/', classic_login, name='login'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),

    path('api/', include('api.urls')),
    path('api/auth/', include('ua.urls')),
    path('ua/', include('ua.urls')),

    path('api/auth/login/', obtain_auth_token),
    path('limited/', rate_limit, name='rate_limit'),
    path('portfolio/upload/', upload_profile, name='profile_upload'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
