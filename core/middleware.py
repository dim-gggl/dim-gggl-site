import logging

from django.conf import settings
from django.db import connection, reset_queries
from django.shortcuts import render


logger = logging.getLogger(__name__)


class QueryCountDebugMiddleware:
    """Log an alert when an excessive number of SQL queries occur in DEBUG."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            reset_queries()

        response = self.get_response(request)

        if settings.DEBUG:
            num_queries = len(connection.queries)
            if num_queries > 20:
                logger.warning(
                    "High query count detected on %s: %s queries", request.path, num_queries
                )

        return response


class MaintenanceModeMiddleware:
    """Display a maintenance page when MAINTENANCE_MODE is active."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MAINTENANCE_MODE", False):
            if not request.path.startswith("/admin/") and not request.path.startswith("/static/"):
                return render(request, "core/maintenance.html", status=503)

        return self.get_response(request)


class SecurityHeadersMiddleware:
    """Attach security headers such as Content Security Policy."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.DEBUG and getattr(settings, "CONTENT_SECURITY_POLICY", ""):
            response.setdefault("Content-Security-Policy", settings.CONTENT_SECURITY_POLICY)
        return response

