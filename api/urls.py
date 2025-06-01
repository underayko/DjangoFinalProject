from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_items, get_item, add_item, update_item, delete_item, RegisterView, ItemViewSet, PostViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
   path('items/', get_items, name='get_items'),
    path('items/<int:item_id>/', get_item, name='get_item'),
    path('add_item/', add_item, name='add_item'),
    path('update_item/<int:item_id>/', update_item, name='update_item'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
