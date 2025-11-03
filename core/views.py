import logging
import random

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from projects.models import Project, Technology

logger = logging.getLogger("portfolio")


class HomeView(TemplateView):
    """
    Homepage view with featured projects and tech stack.
    Uses centralized settings for personal info.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured projects with optimized query
        projects_list = [proj.id for proj in Project.published.filter(is_featured=True)]
        featured_ids = []
        while len(featured_ids) < settings.FEATURED_PROJECTS_COUNT:
            idx = random.randint(0, len(projects_list) - 1)
            featured_ids.append(projects_list.pop(idx))
        featured_projects = [Project.published.get(id=id) for id in featured_ids]

        context["featured_projects"] = featured_projects

        # Tech stack for homepage
        context["tech_backend"] = (
            Technology.objects.filter(category__in=["backend", "language"])
            .order_by("-proficiency", "name")
            .values_list("name", flat=True)
        )

        context["tech_data_tools"] = (
            Technology.objects.filter(category__in=["database", "tool"])
            .order_by("-proficiency", "name")
            .values_list("name", flat=True)
        )

        return context


@method_decorator(cache_page(60 * 60), name="dispatch")
class AboutView(TemplateView):
    """About page with technologies breakdown."""

    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistics
        context["total_projects"] = Project.published.count()
        context["technologies_count"] = Technology.objects.count()
        context["years_experience"] = settings.PORTFOLIO_PERSON["years_experience"]
        

        # Technologies by category with color gradient based on proficiency
        context["backend_techs"] = self._add_skill_colors(
            Technology.objects.filter(
                category__in=["backend", "language"]
            ).order_by("-proficiency", "name")
        )

        context["frontend_techs"] = self._add_skill_colors(
            Technology.objects.filter(category="frontend").order_by("-proficiency", "name")
        )

        context["database_techs"] = self._add_skill_colors(
            Technology.objects.filter(category="database").order_by("-proficiency", "name")
        )

        context["tools"] = self._add_skill_colors(
            Technology.objects.filter(category="tool").order_by("-proficiency", "name")
        )

        return context

    def _add_skill_colors(self, technologies):
        """
        Add gradient colors to technologies based on proficiency level.
        Higher proficiency = more vibrant colors
        """
        color_map = {
            5: {"from": "#00ff88", "to": "#00cc6a"},  # Vert vif
            4: {"from": "#00e1ff", "to": "#00b8d4"},  # Cyan vif
            3: {"from": "#ffa500", "to": "#ff8c00"},  # Orange
            2: {"from": "#ff6b6b", "to": "#ee5a5a"},  # Rouge-orange
            1: {"from": "#888888", "to": "#666666"},  # Gris terne
        }

        tech_list = []
        for tech in technologies:
            tech_dict = {
                "name": tech.name,
                "proficiency": tech.proficiency,
                "color_from": color_map.get(tech.proficiency, color_map[3])["from"],
                "color_to": color_map.get(tech.proficiency, color_map[3])["to"],
            }
            tech_list.append(tech_dict)

        return tech_list


class CompetencesView(TemplateView):
    """Skills/competences page."""

    template_name = "core/competences.html"




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
    return HttpResponse("Trop de requêtes. Veuillez réessayer plus tard.", status=429)

