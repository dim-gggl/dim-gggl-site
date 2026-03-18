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

VIBE_PROJECT_SLUGS = [
    "sunoreverse",
    "suno-arch",
    "market-pal",
    "KinoLOG",
]

CLI_PROJECT_SLUGS = [
    "epic_events",
    "AlgoInvest-Trade",
    "Chess_Up",
    "Book_Scraper",
    "clinkey-cli",
    "yotta",
    "super-pocket",
    "video-specs"
]

DJANGO_TECH_SLUGS = ["django", "django-rest-framework"]
FEATURED_PROJECTS_COUNT = 4


def _ordered_projects_by_slugs(slugs):
    projects = (
        Project.published.select_related("category")
        .prefetch_related("technologies")
        .filter(slug__in=slugs)
    )
    projects_by_slug = {
        project.slug: project for project in projects
    }
    return [projects_by_slug[slug] for slug in slugs if slug in projects_by_slug]


def _top_technologies(categories, limit=6):
    return (
        Technology.objects.filter(category__in=categories)
        .order_by("-proficiency", "name")
        .values_list("name", flat=True)[:limit]
    )


def _random_featured_projects(limit=FEATURED_PROJECTS_COUNT):
    featured_projects = list(
        Project.published.select_related("category")
        .prefetch_related("technologies")
        .filter(is_featured=True)
    )
    selection_size = min(len(featured_projects), limit)
    if not selection_size:
        return []
    return random.sample(featured_projects, selection_size)


class HomeView(TemplateView):
    """Homepage view with a short introduction and navigation hub."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_projects"] = _random_featured_projects()
        context["home_intro"] = {
            "title": "dim-gggl",
            "body": (
                "Backend Python developer building Django applications, CLI tools, "
                "and AI-assisted creative workflows."
            ),
        }
        context["navigation_sections"] = [
            {
                "eyebrow": "Explore",
                "title": "IA",
                "description": "Prompting, music, video, jailbreaks, and vibe-engineering.",
                "url": reverse("core:ai"),
            },
            {
                "eyebrow": "Build",
                "title": "CLI",
                "description": "A curated selection of command-line oriented projects.",
                "url": reverse("core:cli"),
            },
            {
                "eyebrow": "Ship",
                "title": "Django",
                "description": "Published Django and DRF projects from the portfolio.",
                "url": reverse("core:django"),
            },
            {
                "eyebrow": "Browse",
                "title": "Projets",
                "description": "The complete archive with filters, search, and details.",
                "url": reverse("projects:list"),
            },
            {
                "eyebrow": "Profile",
                "title": "A propos",
                "description": "Background, stack, and a broader presentation page.",
                "url": reverse("core:about"),
            },
        ]
        context["archive_url"] = reverse("projects:list")
        return context


class AIView(TemplateView):
    """Editorial AI page with prompting sections and curated projects."""

    template_name = "core/ai.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ai_page"] = {
            "prompting": {
                "intro": {
                    "title": "Prompting",
                    "body": (
                        "A focused page for AI experiments "
                        "built around authored prompts and reverse-analysis workflows."
                    ),
                },
                "music": {
                    "title": "Music",
                    "spotify_embed_url": (
                        "https://open.spotify.com/embed/album/"
                        "5i9pJkPpbr0LzhRMQUHgFc?utm_source=generator"
                    ),
                    "spotify_external_url": (
                        "https://open.spotify.com/album/"
                        "5i9pJkPpbr0LzhRMQUHgFc"
                    ),
                    "spotify_caption": "Artist mapping EP on Spotify.",
                    "track_title": "Un mot",
                    "style_prompt": (
                        "Dark cinematic French chanson with textured synths, "
                        "intimate male vocals, restrained pulse, and a haunted "
                        "late-night atmosphere."
                    ),
                    "lyrics_prompt": "",
                },
                "video": {
                    "title": "Video",
                    "body": (
                        "A direct entry point to the Sora experiments and video-oriented "
                        "prompting work."
                    ),
                    "sora_url": "https://sora.chatgpt.com/profile/dim-gggl",
                    "cta_label": "Voir ma page Sora",
                },
                "jailbreak": {
                    "title": "Jailbreak",
                    "body": (
                        "I train to understand how LLMs work by iterating on different kind "
                        "of prompts and from time to time I jailbreak the model to understand."
                        "\n(For obvious reasons, parts of the answer from the model have been erased)"
                    ),
                    "screenshot_path": "static/images/Jailbreak_grok.",
                    "image_alt": "Exemple of a conversation with a jailbreak version of Grok",
                },
            },
            "vibe_engineering": {
                "title": "Vibe-Engineering",
                "body": (
                    "Projects built on Google AI Studio with Gemini 3 Pro and Gemini 3.1 Pro "
                    "so just with prompting and iterations."
                ),
                "project_slugs": VIBE_PROJECT_SLUGS,
            },
        }
        context["vibe_projects"] = _ordered_projects_by_slugs(VIBE_PROJECT_SLUGS)
        return context


class CLIProjectsView(TemplateView):
    """Curated CLI portfolio page."""

    template_name = "core/cli.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = _ordered_projects_by_slugs(CLI_PROJECT_SLUGS)
        context["page_intro"] = {
            "title": "CLI",
            "body": (
                "A first-release selection of command-line projects focused on "
                "workflow, ergonomics, and packaging."
            ),
        }
        context["projects"] = projects
        context["missing_project_count"] = len(CLI_PROJECT_SLUGS) - len(projects)
        return context


class DjangoProjectsView(TemplateView):
    """Published Django and DRF project page."""

    template_name = "core/django.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_intro"] = {
            "title": "Django",
            "body": (
                "Projects built with Django and Django REST Framework, ordered as part "
                "of the published portfolio."
            ),
        }
        context["projects"] = (
            Project.published.select_related("category")
            .prefetch_related("technologies")
            .filter(technologies__slug__in=DJANGO_TECH_SLUGS)
            .order_by("order", "-completed_at")
            .distinct()
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
            Technology.objects.filter(category__in=["backend", "language"]).order_by(
                "-proficiency", "name"
            )
        )

        context["frontend_techs"] = self._add_skill_colors(
            Technology.objects.filter(category="frontend").order_by(
                "-proficiency", "name"
            )
        )

        context["database_techs"] = self._add_skill_colors(
            Technology.objects.filter(category="database").order_by(
                "-proficiency", "name"
            )
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
