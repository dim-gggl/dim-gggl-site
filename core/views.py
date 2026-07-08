import logging

from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import get_language
from django.views.generic import TemplateView

from core.localization.translation_service import translate_text

logger = logging.getLogger("portfolio")


class SpaView(TemplateView):
    """
    Serve the React single-page application shell.

    All page content is fetched by the frontend from the JSON API
    (see the ``api`` app); this view only renders the HTML shell with
    SEO meta tags and the built frontend assets.
    """

    template_name = "core/spa.html"


class RobotsTxtView(TemplateView):
    """Serve the robots.txt content dynamically."""

    def get(self, request, *args, **kwargs):
        sitemap_url = request.build_absolute_uri(reverse("sitemap"))
        lines = [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {sitemap_url}",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")


def ratelimit_error(request, exception=None):
    """Custom error page for rate-limited requests."""
    return HttpResponse(
        translate_text(
            "Too many requests. Please try again later.",
            getattr(request, "LANGUAGE_CODE", get_language()),
        )
        or "Too many requests. Please try again later.",
        status=429,
    )
