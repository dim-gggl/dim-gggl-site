from django.contrib.sitemaps import Sitemap

from .models import Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj: Project):
        return obj.updated_at


