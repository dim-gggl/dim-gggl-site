from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from projects.models import Project, Technology
from .forms import ContactForm
from .decorators import rate_limit


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = {
            'name': 'Dimitri Gaggioli',
            'title': 'Développeur Python - Backend',
            'baseline': 'Think. Code. Push.',
            'location': 'Paris 2e',
            'contact_email': 'dimitri.gaggioli@gmail.com',
            'contact_phone': '+33 6 20 15 61 72',
            'github': 'https://github.com/dim-gggl',
            'linkedin': 'https://www.linkedin.com/in/dimitri-gaggioli/',
        }
        context['tech_backend'] = ['Python', 'Django', 'Flask', 'DRF', 'FastAPI']
        context['tech_data_tools'] = [
            'PostgreSQL', 
            'MySQL', 
            'SQLite', 
            'SQLAlchemy', 
            'Git', 
            'GitHub', 
            'pytest',
            'poetry',
            'uv', 
            'Docker', 
            'CI/CD',
            'Claude Code',
            'Cursor',
            'Codex'
        ]
        context['featured_projects'] = (
            Project.objects.filter(is_featured=True, is_published=True)
            .select_related('category')
            .prefetch_related('technologies')
            .order_by('order')[:4]
        )
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_projects'] = Project.objects.filter(is_published=True).count()
        context['technologies_count'] = Technology.objects.count()
        context['years_experience'] = 3

        context['backend_techs'] = Technology.objects.filter(
            category__in=['backend', 'language']
        ).order_by('-proficiency', 'name')

        context['frontend_techs'] = Technology.objects.filter(
            category='frontend'
        ).order_by('-proficiency', 'name')

        context['database_techs'] = Technology.objects.filter(
            category='database'
        ).order_by('-proficiency', 'name')

        context['tools'] = Technology.objects.filter(
            category='tool'
        ).order_by('-proficiency', 'name')
        return context


class CompetencesView(TemplateView):
    template_name = 'core/competences.html'


@method_decorator(rate_limit(key_prefix='contact_form', limit=3, period=3600), name='post')
class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "✓ Message sent successfully! I will reply as soon as possible."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "❌ An error occurred. Please check the form fields."
        )
        return super().form_invalid(form)


class RobotsTxtView(TemplateView):
    """Serve the robots.txt content dynamically."""

    def get(self, request, *args, **kwargs):
        sitemap_url = request.build_absolute_uri(reverse('sitemap'))
        lines = [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {sitemap_url}",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")
