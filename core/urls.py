from django.urls import path

from .views import SpaView

app_name = "core"

urlpatterns = [
    path("", SpaView.as_view(), name="home"),
    path("ai/", SpaView.as_view(), name="ai"),
    path("cli/", SpaView.as_view(), name="cli"),
    path("django/", SpaView.as_view(), name="django"),
    path("about/", SpaView.as_view(), name="about"),
    path("skills/", SpaView.as_view(), name="skills"),
]
