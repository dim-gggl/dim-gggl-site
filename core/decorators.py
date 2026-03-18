from functools import wraps

from django.core.cache import cache
from django.http import HttpResponseForbidden

from core.localization.translation_service import translate_text


def rate_limit(key_prefix, limit=5, period=3600):
    """Simple cache-backed rate limiter decorator."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            identifier = request.META.get("REMOTE_ADDR", "unknown")
            cache_key = f"{key_prefix}:{identifier}"
            attempts = cache.get(cache_key, 0)
            if attempts >= limit:
                return HttpResponseForbidden(
                    translate_text(
                        "Too many requests. Please try again later.",
                        getattr(request, "LANGUAGE_CODE", None),
                    )
                    or "Too many requests. Please try again later."
                )
            cache.set(cache_key, attempts + 1, period)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
