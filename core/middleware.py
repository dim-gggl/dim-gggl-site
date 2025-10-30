import logging

from django.conf import settings
from django.db import connection, reset_queries
from django.shortcuts import render

logger = logging.getLogger('portfolio')


class QueryCountDebugMiddleware:
    """
    Log a warning when an excessive number of SQL queries occur.
    Only active in DEBUG mode.
    """

    QUERY_THRESHOLD = 20

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            reset_queries()

        response = self.get_response(request)

        if settings.DEBUG:
            num_queries = len(connection.queries)
            if num_queries > self.QUERY_THRESHOLD:
                logger.warning(
                    f"High query count on {request.path}: {num_queries} queries"
                )
                
                # In DEBUG, also log the queries
                for i, query in enumerate(connection.queries, 1):
                    logger.debug(f"Query {i}: {query['sql'][:100]}...")

        return response


class MaintenanceModeMiddleware:
    """
    Display a maintenance page when MAINTENANCE_MODE setting is True.
    Allows admin access.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MAINTENANCE_MODE", False):
            # Allow admin access and static files
            if not (request.path.startswith("/admin/") or request.path.startswith("/static/")):
                logger.info(f"Maintenance mode: Blocked access to {request.path}")
                return render(request, "core/maintenance.html", status=503)

        return self.get_response(request)


class SecurityHeadersMiddleware:
    """Add security headers like Content Security Policy."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only add CSP in production
        if not settings.DEBUG and getattr(settings, "CONTENT_SECURITY_POLICY", ""):
            response.setdefault("Content-Security-Policy", settings.CONTENT_SECURITY_POLICY)
        
        return response