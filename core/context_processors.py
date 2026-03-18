from django.conf import settings
from django.utils.translation import get_language

from core.localization.translation_service import normalize_language_code


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
        "current_language": normalize_language_code(get_language()),
        "available_languages": tuple(settings.LANGUAGES),
    }
