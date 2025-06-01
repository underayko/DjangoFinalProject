from django.core.cache import cache
from django.http import JsonResponse
from functools import wraps
import time

def rate_limit(max_requests=5, timeframe=60):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate-limit:{ip}:{view_func.__name__}"
            history = cache.get(key, [])
            current_time = time.time()

            # Remove old entries
            history = [timestamp for timestamp in history if current_time - timestamp < timeframe]

            if len(history) >= max_requests:
                return JsonResponse({
                    'success': False,
                    'message': 'Too many requests. Try again later.'
                }, status=429)

            # Add current request time
            history.append(current_time)
            cache.set(key, history, timeout=timeframe)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
