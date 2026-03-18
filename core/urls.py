from django.urls import path
from .views import AIView, AboutView, CLIProjectsView, CompetencesView, DjangoProjectsView, HomeView


app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("ai/", AIView.as_view(), name="ai"),
    path("cli/", CLIProjectsView.as_view(), name="cli"),
    path("django/", DjangoProjectsView.as_view(), name="django"),
    path("about/", AboutView.as_view(), name="about"),
    path("skills/", CompetencesView.as_view(), name="skills"),
]
