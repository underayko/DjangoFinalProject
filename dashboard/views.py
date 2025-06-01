from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TestEntry
from .decorators import rate_limit
from ua.forms import ProfilePhotoForm
from ua.models import UserProfile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.views import rate_limit
from .models import Profile
from django.views.decorators.csrf import csrf_exempt


@login_required
def dashboard_home(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def dashboard_view(request):
    """Student dashboard - for regular users"""
    # If user is admin, redirect to admin area
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/admin-home/')
    
    data = [
        {"title": "Users", "count": 150},
        {"title": "Orders", "count": 320},
        {"title": "Revenue", "count": "₱12,450"},
    ]
    return render(request, 'dashboard/dashboard.html', {"data": data})

# def crud_test_view(request):
#     if request.method == 'POST':
#         entry_id = request.POST.get('entry_id')
#         name = request.POST.get('name')
#         if entry_id:  # If entry_id exists, we are updating
#             entry = get_object_or_404(TestEntry, id=entry_id)
#             entry.name = name
#             entry.save()
#         else:  # Otherwise, create new
#             if name:
#                 TestEntry.objects.create(name=name)
#         return redirect('crud_test')

#     entries = TestEntry.objects.all()
#     return render(request, 'dashboard/crud_test.html', {'entries': entries})




# @csrf_exempt
# def crud_test_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data from the body
#             data = json.loads(request.body)
#             entry_id = data.get('entry_id')
#             name = data.get('name')

#             if entry_id:  # Update existing entry
#                 entry = get_object_or_404(TestEntry, id=entry_id)
#                 entry.name = name
#                 entry.save()
#                 return JsonResponse({'success': True, 'message': f'Entry {entry_id} updated successfully.'})

#             elif name:  # Create new entry
#                 new_entry = TestEntry.objects.create(name=name)
#                 return JsonResponse({'success': True, 'message': f'Entry {new_entry.id} created successfully.'})

#             return JsonResponse({'success': False, 'message': 'Name field is required.'}, status=400)

#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON format'}, status=400)

#     # GET request to show all entries
#     entries = TestEntry.objects.all()
#     return render(request, 'dashboard/crud_test.html', {'entries': entries})

@csrf_exempt
def crud_test_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        entry_id = data.get('entry_id')
        name = data.get('name')

        if not name:
            return JsonResponse({'success': False, 'message': 'Name is required'}, status=400)

        if entry_id:
            try:
                entry = TestEntry.objects.get(id=entry_id)
                entry.name = name
                entry.save()
                return JsonResponse({'success': True, 'message': f"Entry {entry_id} updated successfully."})
            except TestEntry.DoesNotExist:
                return JsonResponse({'success': False, 'message': f"Entry with ID {entry_id} not found."}, status=404)
        else:
            entry = TestEntry.objects.create(name=name)
            return JsonResponse({'success': True, 'message': f"Entry {entry.id} created successfully."})
    else:
        entries = TestEntry.objects.all().values('id', 'name')
        return JsonResponse({'entries': list(entries)})

def delete_entry_view(request, entry_id):
    TestEntry.objects.filter(id=entry_id).delete()
    return redirect('crud_test')

def reports_view(request):
    return render(request, 'dashboard/reports.html')

def settings_view(request):
    return render(request, 'dashboard/settings.html')

# Activity 1: Portfolio Page

@login_required
def portfolio_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('portfolio')
    else:
        form = ProfilePhotoForm(instance=user_profile)

    return render(request, 'dashboard/portfolio.html', {
        'user_profile': user_profile,
        'form': form,
    })


@rate_limit(max_requests=5, timeframe=60)
def rate_limit(request):
    return JsonResponse({'message': 'You are within the rate limit!'})


# Removed duplicate admin_home function - it's now in Act2/views.py as admin_home_view

@csrf_exempt
def upload_profile(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            photo = request.FILES.get('photo')

            if not name or not photo:
                return JsonResponse({'success': False, 'message': 'Missing name or photo'}, status=400)

            profile = Profile.objects.create(name=name, photo=photo)
            return JsonResponse({
                'success': True,
                'message': f"Uploaded for {profile.name}",
                'photo_url': profile.photo.url
            })

        except Exception as e:
            # This helps you debug!
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)