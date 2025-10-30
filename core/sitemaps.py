from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static or semi-static core views."""

    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "core:skills",
            "core:contact",
            "projects:list",
        ]

    def location(self, item):
        return reverse(item)

