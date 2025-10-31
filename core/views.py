import logging

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django_ratelimit.decorators import ratelimit

from projects.models import Project, Technology
from .forms import ContactForm
from .utils import get_client_ip

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
        context["featured_projects"] = (
            Project.published.filter(is_featured=True)
            .select_related("category")
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
                "category__name",
            )
            .order_by("order")[: settings.FEATURED_PROJECTS_COUNT]
        )

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

        # Technologies by category
        context["backend_techs"] = Technology.objects.filter(
            category__in=["backend", "language"]
        ).order_by("-proficiency", "name")

        context["frontend_techs"] = Technology.objects.filter(
            category="frontend"
        ).order_by("-proficiency", "name")

        context["database_techs"] = Technology.objects.filter(
            category="database"
        ).order_by("-proficiency", "name")

        context["tools"] = Technology.objects.filter(category="tool").order_by(
            "-proficiency", "name"
        )

        return context


class CompetencesView(TemplateView):
    """Skills/competences page."""

    template_name = "core/competences.html"


@method_decorator(
    ratelimit(key="ip", rate="3/h", method="POST", block=True), name="post"
)
class ContactView(FormView):
    """
    Contact form view with rate limiting and logging.
    Uses django-ratelimit instead of custom decorator.
    """

    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("core:contact")

    def form_valid(self, form):
        """Save the contact message with IP tracking."""
        contact_message = form.save(commit=False)
        contact_message.ip_address = get_client_ip(self.request)
        contact_message.save()

        logger.info(
            f"Contact form submitted by {contact_message.name} "
            f"({contact_message.email}) from IP {contact_message.ip_address}"
        )

        messages.success(
            self.request,
            "✓ Message sent successfully! I will reply as soon as possible.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Log invalid form submissions."""
        logger.warning(
            f"Invalid contact form submission from IP {get_client_ip(self.request)}: "
            f"{form.errors}"
        )
        messages.error(
            self.request, "❌ An error occurred. Please check the form fields."
        )
        return super().form_invalid(form)


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
