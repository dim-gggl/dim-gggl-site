import logging
import random

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from core.localization.translation_service import translate_text
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
    return [
        projects_by_slug[slug] for slug in slugs if slug in projects_by_slug
        ]


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
                "title": "AI",
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
                "title": "Projects",
                "description": "The complete archive with filters, search, and details.",
                "url": reverse("projects:list"),
            },
            {
                "eyebrow": "Profile",
                "title": "About",
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
                        "A focused page for AI experiments built around "
                        "authored prompts and reverse-analysis workflows."
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
                    "spotify_caption": ("The artist Nola, now available on every music "
                                        "platform is a fictional artist with all the "
                                        "generated music I made through Suno AI"),
                    "track_title": "Un mot",
                    "style_prompt": (
                        "The Style Prompt:\n\n"
                        "Alternative Electronic, Atmospheric IDM, Experimental Melodic "
                        "Ambient, Ternary Rhythm, 6/8 time signature, Jazz chords, "
                        "Prophet 6, Moog Matriarch, Eurorack Modular System, Roland "
                        "Space Echo, Modular Synthesizer, glitchy gentle drum kit, "
                        "electric guitar ambient swells, electric bass guitar, tape echo, "
                        "falsetto male vocals, breathy and resonant, ethereal, intimate, "
                        "French lyrics, minor key, building emotional crescendo, whispered "
                        "intro and outro, spacious mix. \n-rock, -pop, -radio, -lyrical vocal, "
                        "-choirs, -violin, -binary rhythm, -4/4 time signature, -yelling, "
                        "-shouting, -operatic, -happy, -radio, -pop\n\n"
                        "Weirdness: 6%\nStyle: 85%"
                    ),
                    "lyrics_prompt": """
--------------------------------
Lyrics Prompt:

[Mood: Melancholic] [Energy: Low]
[Instrument: Analog Synth, Space Echo, Soft Drums]

[Intro]
(misty atmosphere, slow analog synth arpeggiator building)

[Instrumental Break]
(relentless analog synth arpeggiator, reverb swells)

[Verse 1 | Whispered, Intimate]
(falsetto, floating delivery)
Il suffirait d'un mot
Pour que du monde
L'ordre chancelle
Possible ou rien
À vue perdue
Et qu'infinis
S'ouvrent les champs

Il suffirait d'un mot
Parmi les plus petits qui soient
De ceux tu sais
Qui ne sont pas
Labiaux mais qui sont ronds et chauds

[Pre-Chorus | Build-Up]
(space echo swells, instruments rising)
Il suffit de ce mot, oui
Décoré de l'écrin
Des velours de ton grain
Habillé d'abandon

[Chorus | Energy: Medium]
(ethereal, resonant, full reverb)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Instrumental Break]
(synth arpeggiator reprises, echo trails)

[Verse 2 | Whispered, Intimate]
(breathy, close-mic)
Oui c'est ce mot-là qu'il faudrait
Né de ta voix
Battu dans mes tempes
Comme un vieux métronome
Que n'atteint pas l'usure

Qui se fait désirer
À coups de litanies
Et qui rappelle au temps
Ce qu'il lui doit encore

[Bridge | Breakdown]
(sparse, drums enter softly, voice alone)
Combien tu ne le dis pas...
Combien tu ne le dis pas...
Combien tu ne le dis pas...

[Chorus | Energy: High]
(ethereal, resonant, fuller arrangement)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Bridge | Energy: Medium]
(building slowly, emotional tension)
Il suffit de ta bouche
Pour laisser passer l'air
Et qui dans mon oreille
Viendra lui donner forme

[Final Chorus | Energy: High | Harmonies]
(full band, maximum emotional release)
Sponte année… délicat...
Venu là déposé
Comme par l'évidence
Pour que s'écroule ma fierté
Et qu'à genoux
Je ne sois qu'à toi

[Outro | Energy: Low]
(fading, whispered, instruments dissolving)
Une forme précieuse...
Qui te ressemblerait...

[End]
(hold last word; leave room for Studio fade)
                    """,
                },
                "video": {
                    "title": "Video",
                    "body": (
                        "A direct entry point to the Sora experiments and video-oriented "
                        "prompting work."
                    ),
                    "sora_url": "https://sora.chatgpt.com/profile/dim-gggl",
                    "cta_label": "Open my Sora page",
                },
                "jailbreak": {
                    "title": "Jailbreak",
                    "body": (
                        "I train to understand how LLMs work by iterating on "
                        "different kinds of prompts and, from time to time, I "
                        "jailbreak the model to understand its limits.\n"
                        "(For obvious reasons, parts of the model answer have "
                        "been erased.)"
                    ),
                    "screenshot_path": "static/images/Jailbreak_grok.",
                    "image_alt": "Example of a conversation with a jailbroken version of Grok",
                },
            },
            "vibe_engineering": {
                "title": "Vibe Engineering",
                "body": (
                    "Projects built on Google AI Studio with Gemini 3 Pro so "
                    "mostly through prompting and iteration."
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
        intro_body = (
            "Projects built with Django and Django REST Framework, both from "
            "personal projects and study projects."
        )
        context["page_intro"] = {
            "title": "Django",
            "body": (
                translate_text(
                    intro_body,
                    getattr(self.request, "LANGUAGE_CODE", None),
                )
                or intro_body
            ),
        }
        context["projects"] = (
            Project.published.select_related("category")
            .prefetch_related("technologies")
            .filter(technologies__slug__in=DJANGO_TECH_SLUGS)
            .order_by("order", "-completed_at")
            .distinct()
        )
        context["total_projects"] = Project.published.count()
        context["technologies_count"] = Technology.objects.count()
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
    return HttpResponse(
        translate_text(
            "Too many requests. Please try again later.",
            getattr(request, "LANGUAGE_CODE", get_language()),
        )
        or "Too many requests. Please try again later.",
        status=429,
    )
