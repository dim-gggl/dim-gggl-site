from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from .models import Project, Technology, Category


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProjectListView(ListView):
    """List projects with advanced filtering and sorting."""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Project.objects.filter(is_published=True)
            .select_related("category")
            .prefetch_related("technologies")
        )

        # Multiple technology filters
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

        # Technologies with project counts
        context["technologies"] = (
            Technology.objects.annotate(
                project_count=Count("projects", filter=Q(projects__is_published=True))
            )
            .filter(project_count__gt=0)
            .order_by("-project_count", "name")
        )

        # Categories with counts
        context["categories"] = (
            Category.objects.annotate(
                project_count=Count("projects", filter=Q(projects__is_published=True))
            )
            .filter(project_count__gt=0)
            .order_by("order", "name")
        )

        # Active filters and stats
        context["active_tech_slugs"] = self.request.GET.getlist("tech")
        context["active_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "order")
        context["total_projects"] = Project.objects.filter(is_published=True).count()
        context["filtered_count"] = self.get_queryset().count()

        return context


class ProjectDetailView(DetailView):
    """Display a single project's detail page with neighbors and similar projects."""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Project.objects.filter(is_published=True)
            .select_related("category")
            .prefetch_related("technologies", "gallery_images")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.object

        # Similar projects: prioritize same category + shared technologies
        similar_qs = Project.objects.filter(is_published=True).exclude(id=project.id)
        similar_with_tech = (
            similar_qs.filter(
                category=project.category, technologies__in=project.technologies.all()
            )
            .distinct()
            .order_by("order", "-completed_at")[:3]
        )

        if similar_with_tech.count() < 3:
            remaining = 3 - similar_with_tech.count()
            similar_same_cat = (
                similar_qs.filter(category=project.category)
                .exclude(id__in=similar_with_tech.values_list("id", flat=True))
                .order_by("order", "-completed_at")[:remaining]
            )
            context["similar_projects"] = list(similar_with_tech) + list(similar_same_cat)
        else:
            context["similar_projects"] = list(similar_with_tech)

        # Previous and next projects according to ordering
        ordered = Project.objects.filter(is_published=True).order_by("order", "-completed_at")
        ids = list(ordered.values_list("id", flat=True))
        try:
            idx = ids.index(project.id)
            if idx > 0:
                context["previous_project"] = ordered[idx - 1]
            if idx < len(ids) - 1:
                context["next_project"] = ordered[idx + 1]
        except ValueError:
            pass

        return context
