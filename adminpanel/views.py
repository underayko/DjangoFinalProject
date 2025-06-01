from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Event, Student, Attendance
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date, datetime
from django.utils import timezone

def admin_home(request):
    events = Event.objects.all()
    now = timezone.now()
    return render(request, 'adminpanel/home.html', {'events': events, 'now': now})
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event_date = data.get('date')
        event_time = data.get('time')
        datetime_str = f"{event_date} {event_time}"

        if datetime.strptime(datetime_str, "%Y-%m-%d %H:%M") < datetime.now():
            return JsonResponse({'error': 'Cannot set event in the past.'}, status=400)

        event = Event.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            speaker=data.get('speaker'),
            date=event_date,
            time=event_time
        )
        return JsonResponse({'message': 'Event created successfully.'})

    return HttpResponseBadRequest('Invalid request')

@csrf_exempt
def scan_qr(request, event_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        event = get_object_or_404(Event, id=event_id)
        student = get_object_or_404(Student, student_id=student_id)

        attendance, created = Attendance.objects.get_or_create(
            event=event, student=student
        )

        if not created:
            return JsonResponse({'message': 'Already scanned.'})

        return JsonResponse({'message': 'Attendance recorded.'})

    return HttpResponseBadRequest('Invalid method')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendance.objects.filter(event=event).select_related('student')
    return render(request, 'admin/event_detail.html', {
        'event': event,
        'attendees': attendees
    })
