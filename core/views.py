from django.views.generic import TemplateView

from projects.models import Project


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = {
            'name': 'Dimitri Gaggioli',
            'title': 'Développeur Python - Backend',
            'baseline': 'Vite, propre, testé',
            'location': 'Paris 2e',
            'contact_email': 'dimitri.gaggioli@gmail.com',
            'contact_phone': '+33 6 20 15 61 72',
            'github': 'dim-gggl',
        }
        context['tech_backend'] = ['Python', 'Django', 'Flask', 'DRF', 'FastAPI']
        context['tech_data_tools'] = ['PostgreSQL', 'SQLAlchemy', 'Git', 'GitHub', 'pytest', 'uv']
        context['featured_projects'] = (
            Project.objects.filter(is_featured=True).order_by('order')[:4]
        )
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(TemplateView):
    template_name = 'core/contact.html'

from django.shortcuts import render

# Create your views here.
