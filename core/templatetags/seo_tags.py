"""Template tags for rendering SEO meta tags across the site."""

from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language

from core.localization.translation_service import normalize_language_code, translate_key


register = template.Library()


DEFAULT_IMAGE_PATH = "images/og-default.jpg"
DEFAULT_SITE_NAME = "Dimitri Gaggioli - Portfolio"
DEFAULT_TWITTER_HANDLE = "@dim_gggl"


def _safe_static(path: str) -> str:
    """
    Resolve a static path without failing when the manifest is unavailable.

    Args:
        path: Relative static asset path.

    Returns:
        str: Static asset URL.
    """

    try:
        return static(path)
    except ValueError:
        return f"{settings.STATIC_URL}{path}"


def _absolute_url(request, url: str) -> str:
    """Return an absolute URL based on the current request."""

    if not url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if request is None:
        base_url = getattr(settings, "SITE_URL", "")
        return urljoin(base_url, url)
    return request.build_absolute_uri(url)


@register.inclusion_tag("core/components/meta_tags.html", takes_context=True)
def seo_meta_tags(
    context, title=None, description=None, image=None, page_type="website"
):
    """Render SEO, Open Graph, and Twitter meta tags."""
    request = context.get("request")
    language_code = normalize_language_code(
        getattr(request, "LANGUAGE_CODE", None) or get_language()
    )

    default_image_url = _absolute_url(
        request,
        _safe_static(DEFAULT_IMAGE_PATH),
    )

    resolved_image = _absolute_url(request, image) if image else default_image_url

    if request is not None:
        current_url = request.build_absolute_uri()
    else:
        current_url = getattr(settings, "SITE_URL", "") or ""

    return {
        "title": title or translate_key("seo.default_title", language_code),
        "description": description
        or translate_key("seo.default_description", language_code),
        "image": resolved_image or default_image_url,
        "url": current_url,
        "type": page_type or "website",
        "site_name": DEFAULT_SITE_NAME,
        "twitter_handle": DEFAULT_TWITTER_HANDLE,
        "keywords": translate_key("seo.keywords", language_code),
        "locale": "fr_FR" if language_code == "fr" else "en_US",
    }
