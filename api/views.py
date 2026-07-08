"""
JSON API consumed by the React frontend.

Every endpoint accepts an optional ``?lang=`` query parameter (``en`` or
``fr``). Dynamic content is localized server-side through the shared
translation catalog, mirroring the behavior of the previous template views.
"""

import logging
import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q
from django.http import Http404, JsonResponse

from core.localization.content_catalog import UI_TRANSLATIONS
from core.localization.translation_service import (
    normalize_language_code,
    translate_text,
)
from projects.models import Category, Project, ProjectImage, Technology

from . import content
from .serializers import (
    serialize_project_card,
    serialize_project_detail,
    serialize_technology,
)

logger = logging.getLogger("portfolio")


def _language(request):
    """Resolve the requested catalog language."""
    return normalize_language_code(
        request.GET.get("lang") or getattr(request, "LANGUAGE_CODE", None)
    )


def _translate_mapping(data, language, skip_keys=frozenset()):
    """Recursively translate every string value of a content mapping."""
    if isinstance(data, dict):
        return {
            key: (
                value
                if key in skip_keys
                else _translate_mapping(value, language, skip_keys)
            )
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [_translate_mapping(item, language, skip_keys) for item in data]
    if isinstance(data, str):
        return translate_text(data, language)
    return data


AI_PAGE_LITERAL_KEYS = frozenset(
    {
        "spotify_embed_url",
        "spotify_external_url",
        "track_title",
        "style_prompt",
        "lyrics_prompt",
        "sora_url",
        "screenshot",
        "image_alt",
    }
)


def _published_projects():
    return Project.published.select_related("category").prefetch_related(
        "technologies"
    )


def _ordered_projects_by_slugs(slugs):
    projects_by_slug = {
        project.slug: project
        for project in _published_projects().filter(slug__in=slugs)
    }
    return [
        projects_by_slug[slug]
        for slug in slugs
        if slug in projects_by_slug
    ]


def site_view(request):
    """Global site payload: person info, UI strings, and stats."""
    language = _language(request)
    return JsonResponse(
        {
            "language": language,
            "languages": [code for code, _ in settings.LANGUAGES],
            "person": settings.PORTFOLIO_PERSON,
            "ui": UI_TRANSLATIONS[language],
            "stats": {
                "projects": Project.published.count(),
                "technologies": Technology.objects.count(),
                "years_experience": (
                    settings.PORTFOLIO_PERSON["years_experience"]
                ),
            },
        }
    )


def home_view(request):
    """Homepage payload: intro, navigation hub, and featured projects."""
    language = _language(request)
    featured = list(_published_projects().filter(is_featured=True))
    selection_size = min(len(featured), content.FEATURED_PROJECTS_COUNT)
    featured = (
        random.sample(featured, selection_size) if selection_size else []
    )

    return JsonResponse(
        {
            "intro": {
                "title": content.HOME_INTRO["title"],
                "body": translate_text(content.HOME_INTRO["body"], language),
            },
            "navigation": [
                {
                    "eyebrow": translate_text(section["eyebrow"], language),
                    "title": translate_text(section["title"], language),
                    "description": translate_text(
                        section["description"], language
                    ),
                    "url": section["url"],
                }
                for section in content.NAVIGATION_SECTIONS
            ],
            "featured": [
                serialize_project_card(project, language)
                for project in featured
            ],
        }
    )


def ai_view(request):
    """AI page payload: prompting sections and vibe-engineering projects."""
    language = _language(request)
    page = _translate_mapping(
        content.AI_PAGE, language, skip_keys=AI_PAGE_LITERAL_KEYS
    )
    page["vibe_engineering"]["projects"] = [
        serialize_project_card(project, language)
        for project in _ordered_projects_by_slugs(content.VIBE_PROJECT_SLUGS)
    ]
    return JsonResponse(page)


def cli_view(request):
    """Curated CLI portfolio payload."""
    language = _language(request)
    projects = _ordered_projects_by_slugs(content.CLI_PROJECT_SLUGS)
    return JsonResponse(
        {
            "intro": {
                "title": content.CLI_PAGE_INTRO["title"],
                "body": translate_text(
                    content.CLI_PAGE_INTRO["body"], language
                ),
            },
            "projects": [
                serialize_project_card(project, language)
                for project in projects
            ],
            "missing_project_count": (
                len(content.CLI_PROJECT_SLUGS) - len(projects)
            ),
        }
    )


def django_view(request):
    """Published Django and DRF projects payload."""
    language = _language(request)
    projects = (
        _published_projects()
        .filter(technologies__slug__in=content.DJANGO_TECH_SLUGS)
        .order_by("order", "-completed_at")
        .distinct()
    )
    return JsonResponse(
        {
            "intro": {
                "title": content.DJANGO_PAGE_INTRO["title"],
                "body": translate_text(
                    content.DJANGO_PAGE_INTRO["body"], language
                ),
            },
            "projects": [
                serialize_project_card(project, language)
                for project in projects
            ],
        }
    )


def about_view(request):
    """About page payload: stats and technologies grouped by category."""
    language = _language(request)

    def tech_group(category_filter):
        technologies = Technology.objects.filter(
            **category_filter
        ).order_by("-proficiency", "name")
        return [
            {
                **serialize_technology(tech, language),
                "color_from": content.SKILL_COLOR_MAP.get(
                    tech.proficiency, content.SKILL_COLOR_MAP[3]
                )["from"],
                "color_to": content.SKILL_COLOR_MAP.get(
                    tech.proficiency, content.SKILL_COLOR_MAP[3]
                )["to"],
            }
            for tech in technologies
        ]

    return JsonResponse(
        {
            "stats": {
                "projects": Project.published.count(),
                "technologies": Technology.objects.count(),
                "years_experience": (
                    settings.PORTFOLIO_PERSON["years_experience"]
                ),
            },
            "skills": {
                "backend": tech_group(
                    {"category__in": ["backend", "language"]}
                ),
                "frontend": tech_group({"category": "frontend"}),
                "database": tech_group({"category": "database"}),
                "tools": tech_group({"category": "tool"}),
            },
        }
    )


def project_list_view(request):
    """Filterable, paginated project list payload."""
    language = _language(request)
    queryset = _published_projects()

    tech_slugs = request.GET.getlist("tech")
    for tech_slug in tech_slugs:
        queryset = queryset.filter(technologies__slug=tech_slug)

    cat_slug = request.GET.get("category")
    if cat_slug:
        queryset = queryset.filter(category__slug=cat_slug)

    search = (request.GET.get("q", "") or "").strip()
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(tagline__icontains=search)
        )

    sort = request.GET.get("sort", "order")
    if sort == "recent":
        queryset = queryset.order_by("-completed_at", "order")
    elif sort == "title":
        queryset = queryset.order_by("title")
    else:
        queryset = queryset.order_by("order", "-completed_at")

    queryset = queryset.distinct()

    paginator = Paginator(queryset, settings.PROJECTS_PER_PAGE)
    page_number = request.GET.get("page") or 1
    page = paginator.get_page(page_number)

    sidebar_cache_key = "api_project_list_sidebar"
    sidebar = cache.get(sidebar_cache_key)
    if sidebar is None:
        technologies = (
            Technology.objects.annotate(
                project_count=Count(
                    "projects", filter=Q(projects__is_published=True)
                )
            )
            .filter(project_count__gt=0)
            .order_by("-project_count", "name")
        )
        categories = (
            Category.objects.annotate(
                project_count=Count(
                    "projects", filter=Q(projects__is_published=True)
                )
            )
            .filter(project_count__gt=0)
            .order_by("order", "name")
        )
        sidebar = {
            "technologies": [
                {
                    "name": tech.name,
                    "slug": tech.slug,
                    "count": tech.project_count,
                }
                for tech in technologies
            ],
            "categories": [
                {
                    "name": category.name,
                    "slug": category.slug,
                    "count": category.project_count,
                }
                for category in categories
            ],
            "total": Project.published.count(),
        }
        cache.set(sidebar_cache_key, sidebar, 60 * 30)

    return JsonResponse(
        {
            "results": [
                serialize_project_card(project, language)
                for project in page.object_list
            ],
            "page": page.number,
            "num_pages": paginator.num_pages,
            "filtered_count": paginator.count,
            "total": sidebar["total"],
            "technologies": sidebar["technologies"],
            "categories": [
                {
                    **category,
                    "name": translate_text(category["name"], language),
                }
                for category in sidebar["categories"]
            ],
        }
    )


def project_detail_view(request, slug):
    """Full project payload with similar projects and prev/next links."""
    language = _language(request)
    gallery_prefetch = Prefetch(
        "gallery_images", queryset=ProjectImage.objects.order_by("order")
    )
    try:
        project = (
            _published_projects()
            .prefetch_related(gallery_prefetch)
            .get(slug=slug)
        )
    except Project.DoesNotExist:
        raise Http404(f"No published project with slug {slug!r}")

    data = serialize_project_detail(project, language)
    data["similar"] = [
        serialize_project_card(similar, language)
        for similar in project.get_similar_projects(
            limit=settings.SIMILAR_PROJECTS_COUNT
        )
    ]

    ordered_slugs = list(
        Project.published.order_by("order", "-completed_at").values_list(
            "slug", "title"
        )
    )
    slugs_only = [item[0] for item in ordered_slugs]
    data["previous"] = data["next"] = None
    try:
        idx = slugs_only.index(project.slug)
        if idx > 0:
            prev_slug, prev_title = ordered_slugs[idx - 1]
            data["previous"] = {"slug": prev_slug, "title": prev_title}
        if idx < len(ordered_slugs) - 1:
            next_slug, next_title = ordered_slugs[idx + 1]
            data["next"] = {"slug": next_slug, "title": next_title}
    except ValueError:
        logger.warning(f"Project {project.slug} not found in ordered list")

    origin = content.ORIGIN_CONTEXTS.get(request.GET.get("from", ""))
    data["origin_context"] = (
        {
            "label": translate_text(origin["label"], language),
            "url": origin["url"],
        }
        if origin
        else None
    )

    return JsonResponse(data)
