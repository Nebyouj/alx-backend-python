# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict
import time

# Configure logger for request logging
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# 1️⃣ Request Logging Middleware
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

# 2️⃣ Restrict Access by Time Middleware
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("21:00", "%H:%M").time()
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Access to chat is restricted outside 6PM to 9PM.")
        return self.get_response(request)

# 3️⃣ Offensive Language / Rate Limiting Middleware
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = defaultdict(list)  # IP → [timestamps]

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/api/conversations/'):
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 1 minute
            self.requests[ip] = [t for t in self.requests[ip] if now - t < 60]
            if len(self.requests[ip]) >= 5:
                return HttpResponseForbidden("Too many messages sent. Please wait.")
            self.requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

# 4️⃣ Role Permission Middleware
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/api/conversations/', '/api/conversations/messages/']
        if request.path.startswith(tuple(protected_paths)):
            user = request.user
            if user.is_authenticated:
                if not hasattr(user, 'role') or user.role not in ['admin', 'moderator']:
                    return HttpResponseForbidden("You do not have the necessary role to access this resource.")
        return self.get_response(request)
