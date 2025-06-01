
# from django.urls import path, include
# from django.urls import path
# from .views import RegisterView, ProtectedView, login_page, signup_page
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# app_name = "ua"

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),      # API register
#     path('login/', TokenObtainPairView.as_view(), name='login'),     # API login
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('protected/', ProtectedView.as_view(), name='protected'),
    
#     # HTML pages for login and signup
#     path('login-page/', login_page, name='login_page'),
#     path('signup-page/', signup_page, name='signup_page'),

# ]

from django.urls import path
from . import views
from .views import RegisterView, ProtectedView, login_page, signup_page, classic_login  # include classic_login
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView


app_name = "ua"

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    # HTML form login/signup
    path('login-page/', login_page, name='login_page'),
    path('signup/', signup_page, name='signup'),
    path('classic-login/', views.classic_login, name='classic_login'),
    
]

