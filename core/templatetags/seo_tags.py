"""Template tags for rendering SEO meta tags across the site."""

from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.templatetags.static import static


register = template.Library()


DEFAULT_TITLE = "Dimitri Gaggioli - Développeur Python Backend"
DEFAULT_DESCRIPTION = (
    "Développeur Python spécialisé en Django, APIs REST et CLIs. "
    "Portfolio de projets web robustes et scalables."
)
DEFAULT_IMAGE_PATH = "images/og-default.jpg"
DEFAULT_SITE_NAME = "Dimitri Gaggioli - Portfolio"
DEFAULT_TWITTER_HANDLE = "@dim_gggl"


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
    context,
    title=None,
    description=None,
    image=None,
    page_type="website"
):
    """Render SEO, Open Graph, and Twitter meta tags."""
    request = context.get("request")

    default_image_url = _absolute_url(
        request,
        static(DEFAULT_IMAGE_PATH),
    )

    resolved_image = _absolute_url(request, image) if image else default_image_url

    if request is not None:
        current_url = request.build_absolute_uri()
    else:
        current_url = getattr(settings, "SITE_URL", "") or ""

    return {
        "title": title or DEFAULT_TITLE,
        "description": description or DEFAULT_DESCRIPTION,
        "image": resolved_image or default_image_url,
        "url": current_url,
        "type": page_type or "website",
        "site_name": DEFAULT_SITE_NAME,
        "twitter_handle": DEFAULT_TWITTER_HANDLE,
    }

