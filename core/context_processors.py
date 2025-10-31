from django.conf import settings


def global_settings(_request):
    """Expose selected settings to templates."""
    return {
        "DEBUG": settings.DEBUG,
        "GOOGLE_ANALYTICS_ID": getattr(settings, "GOOGLE_ANALYTICS_ID", ""),
    }


def site_info(_request):
    """
    Expose portfolio person info to all templates.
    Replaces hardcoded data in views.
    """
    return {
        "person": settings.PORTFOLIO_PERSON,
        "site_url": settings.SITE_URL,
        "years_experience": settings.PORTFOLIO_PERSON.get("years_experience", 0),
    }
