from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@csrf_exempt
def classic_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check user type and redirect accordingly
            if user.is_superuser or user.is_staff:
                return redirect('/admin-home/')  # Redirect to admin home
            else:
                return redirect('/dashboard/')  # Redirect to student dashboard
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    return HttpResponseForbidden("Only POST allowed.")


@staff_member_required
def admin_dashboard_view(request):
    return render(request, 'adminpanel/home.html')  # Use the same template


@login_required
def admin_home_view(request):
    """Admin home page - accessible to both staff and superusers"""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('/dashboard/')  # Redirect non-admin users to student dashboard
    
    return render(request, 'adminpanel/home.html')