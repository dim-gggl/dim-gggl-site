from django.contrib.sitemaps import Sitemap

from django.urls import reverse

from .models import Category, Project


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True).order_by("-completed_at")

    def lastmod(self, obj: Project):
        return obj.updated_at

    def location(self, obj: Project):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj: Category):
        return f"{reverse('projects:list')}?category={obj.slug}"


