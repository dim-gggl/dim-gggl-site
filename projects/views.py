import hashlib
import logging

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Count, Prefetch
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Project, Technology, Category, ProjectImage

logger = logging.getLogger("portfolio")

ORIGIN_CONTEXTS = {
    "ai": {
        "label": "Retour vers IA",
        "url": "core:ai",
    },
    "cli": {
        "label": "Retour vers CLI",
        "url": "core:cli",
    },
    "django": {
        "label": "Retour vers DJANGO",
        "url": "core:django",
    },
}


def make_cache_key(request, prefix="projectlist"):
    """
    Generate a unique cache key based on query parameters.
    This ensures different filter combinations get different caches.
    """
    query_params = request.GET.urlencode()
    cache_key_data = f"{prefix}:{query_params}"
    return f"{prefix}:{hashlib.md5(cache_key_data.encode()).hexdigest()}"


class ProjectListView(ListView):
    """
    List projects with advanced filtering and sorting.
    Uses granular caching based on query parameters.
    """

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = settings.PROJECTS_PER_PAGE

    def get_queryset(self):
        """
        Optimized queryset with selective loading.
        Uses only() to avoid loading unnecessary fields in list view.
        """
        queryset = (
            Project.published.select_related("category")
            .prefetch_related("technologies")
            .only(
                "id",
                "slug",
                "title",
                "tagline",
                "primary_color",
                "secondary_color",
                "featured_image",
                "order",
                "completed_at",
                "is_featured",
                "category__name",
                "category__slug",
            )
        )

        # Multiple technology filters (AND logic)
        tech_slugs = self.request.GET.getlist("tech")
        if tech_slugs:
            for tech_slug in tech_slugs:
                queryset = queryset.filter(technologies__slug=tech_slug)

        # Category filter
        cat_slug = self.request.GET.get("category")
        if cat_slug:
            queryset = queryset.filter(category__slug=cat_slug)

        # Full-text search
        search = (self.request.GET.get("q", "") or "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(tagline__icontains=search)
            )

        # Sorting
        sort = self.request.GET.get("sort", "order")
        if sort == "recent":
            queryset = queryset.order_by("-completed_at", "order")
        elif sort == "title":
            queryset = queryset.order_by("title")
        else:
            queryset = queryset.order_by("order", "-completed_at")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Cache key for sidebar data (changes less frequently)
        sidebar_cache_key = "project_list_sidebar_data"
        sidebar_data = cache.get(sidebar_cache_key)

        if sidebar_data is None:
            # Technologies with project counts
            technologies = (
                Technology.objects.annotate(
                    project_count=Count(
                        "projects", filter=Q(projects__is_published=True)
                    )
                )
                .filter(project_count__gt=0)
                .order_by("-project_count", "name")
            )

            # Categories with counts
            categories = (
                Category.objects.annotate(
                    project_count=Count(
                        "projects", filter=Q(projects__is_published=True)
                    )
                )
                .filter(project_count__gt=0)
                .order_by("order", "name")
            )

            sidebar_data = {
                "technologies": list(technologies),
                "categories": list(categories),
                "total_projects": Project.published.count(),
            }
            cache.set(sidebar_cache_key, sidebar_data, 60 * 30)  # 30 minutes

        context.update(sidebar_data)

        # Active filters and stats
        context["active_tech_slugs"] = self.request.GET.getlist("tech")
        context["active_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "order")
        context["filtered_count"] = self.get_queryset().count()

        return context


class ProjectDetailView(DetailView):
    """
    Display a single project's detail page with optimized similar projects logic.
    """

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """Optimize queries with prefetch of related objects."""
        gallery_prefetch = Prefetch(
            "gallery_images", queryset=ProjectImage.objects.order_by("order")
        )

        return Project.published.select_related("category").prefetch_related(
            "technologies", gallery_prefetch
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Use the model's optimized get_similar_projects method
        context["similar_projects"] = project.get_similar_projects(
            limit=settings.SIMILAR_PROJECTS_COUNT
        )

        # Navigation: previous and next projects
        cache_key = "project_navigation_ids"
        ordered_ids = cache.get(cache_key)

        if ordered_ids is None:
            ordered_ids = list(
                Project.objects.order_by("order", "-completed_at").values_list(
                    "id", "slug"
                )
            )
            cache.set(cache_key, ordered_ids, 60 * 30)  # 30 minutes

        try:
            ids_only = [pid for pid, _ in ordered_ids]
            projects_dict = {
                related_project.id: related_project
                for related_project in Project.published.only("id", "slug", "title")
            }
            idx = ids_only.index(project.id)

            if idx > 0:
                prev_id = ids_only[idx - 1]
                previous_project = projects_dict.get(prev_id)
                if previous_project:
                    context["previous_project"] = {
                        "id": prev_id,
                        "slug": previous_project.slug,
                        "title": previous_project.title,
                    }

            if idx < len(ids_only) - 1:
                next_id = ids_only[idx + 1]
                next_project = projects_dict.get(next_id)
                if next_project:
                    context["next_project"] = {
                        "id": next_id,
                        "slug": next_project.slug,
                        "title": next_project.title,
                    }
        except ValueError:
            logger.warning(f"Project {project.id} not found in ordered list")

        requested_origin = self.request.GET.get("from", "")
        origin_context = ORIGIN_CONTEXTS.get(requested_origin)
        if origin_context:
            context["origin_context"] = {
                "label": origin_context["label"],
                "url": reverse(origin_context["url"]),
            }

        return context
