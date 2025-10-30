from django.conf import settings


def global_settings(_request):
    """Expose selected settings to templates."""

    return {
        'DEBUG': settings.DEBUG,
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
    }

