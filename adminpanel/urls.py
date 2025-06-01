from django.urls import path
from . import views

urlpatterns = [
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/create-event/', views.create_event, name='create_event'),
    path('admin/event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('admin/event/<int:event_id>/scan/', views.scan_qr, name='scan_qr'),
]
