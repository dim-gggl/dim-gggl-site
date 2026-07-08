from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("site/", views.site_view, name="site"),
    path("home/", views.home_view, name="home"),
    path("ai/", views.ai_view, name="ai"),
    path("cli/", views.cli_view, name="cli"),
    path("django/", views.django_view, name="django"),
    path("about/", views.about_view, name="about"),
    path("projects/", views.project_list_view, name="project-list"),
    path(
        "projects/<slug:slug>/",
        views.project_detail_view,
        name="project-detail",
    ),
]
