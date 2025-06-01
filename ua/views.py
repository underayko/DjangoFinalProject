# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth.models import User
# from .serializers import RegisterSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render
# from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_protect
# from .forms import ProfilePhotoForm
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache

# # @csrf_protect
# # def classic_login(request):
# #     if request.method == 'POST':
# #         username = request.POST.get('username')
# #         password = request.POST.get('password')
# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)
# #             return redirect('dashboard')  # Redirect to your dashboard URL name
# #         else:
# #             messages.error(request, "Invalid username or password")
# #     return render(request, 'login.html')
# @never_cache
# @csrf_protect
# def classic_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)

#             # redirect to your admin home page
#             return redirect('admin_home')  # Use your URL name here

#         else:
#             messages.error(request, "Invalid username or password.")
#             return render(request, "login.html")
#     else:
#         return render(request, 'login.html')



# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': serializer.data,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class ProtectedView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         return Response({"message": f"Hello, {request.user.username}! You are authenticated."})

# # Add these views for rendering the HTML forms
# def login_page(request):
#     return render(request, "login.html")

# def signup_page(request):
#     return render(request, "signup.html")

# @login_required
# def upload_photo_view(request):
#     if request.method == 'POST':
#         form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.userprofile)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')  # or anywhere you want
#     else:
#         form = ProfilePhotoForm(instance=request.user.userprofile)
    
#     return render(request, 'ua/upload_photo.html', {'form': form})

# @login_required
# def admin_home(request):
#     return render(request, 'admin/home.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import ProfilePhotoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
import json
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
@never_cache
@csrf_protect
def classic_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Instead of redirecting, return JSON success message for Postman
            return JsonResponse({
                "success": True,
                "message": f"User '{username}' logged in successfully."
            })

        else:
            # Return JSON error message
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password."
            }, status=401)

    else:
        # For GET requests, you can just return a simple message or render form
        return JsonResponse({"message": "Send a POST request with username and password."})

    
@ensure_csrf_cookie
def get_csrf_token(request):
    """Returns a response with CSRF token cookie set (for use in API clients)"""
    if request.method == 'GET':
        return JsonResponse({"message": "CSRF cookie set"})



@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF just for signup
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        

class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! You are authenticated."})

# Add these views for rendering the HTML forms
def login_page(request):
    return render(request, "login.html")

# def signup_page(request):
#     return render(request, "signup.html")

def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('ua:classic_login')  # or your login page URL name
        else:
            # Invalid form, return with errors
            return render(request, 'ua/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'ua/signup.html', {'form': form})


@login_required
def upload_photo_view(request):
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # or anywhere you want
    else:
        form = ProfilePhotoForm(instance=request.user.userprofile)
    
    return render(request, 'ua/upload_photo.html', {'form': form})

# Removed duplicate admin_home function
