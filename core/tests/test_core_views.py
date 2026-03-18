import pytest
from django.urls import reverse

from projects.models import Category, Project, Technology


@pytest.fixture(autouse=True)
def core_view_test_settings(settings):
    settings.COMPRESS_ENABLED = False
    settings.COMPRESS_OFFLINE = False
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }


@pytest.mark.django_db
class TestCoreViews:
    def _make_category(self, name, slug):
        return Category.objects.create(
            name=name,
            slug=slug,
            description=f"{name} category",
        )

    def _make_technology(self, name, slug, category):
        return Technology.objects.create(
            name=name,
            slug=slug,
            category=category,
        )

    def _make_project(
        self,
        title,
        slug,
        category,
        technologies=None,
        is_published=True,
        order=0,
    ):
        project = Project.objects.create(
            title=title,
            slug=slug,
            tagline=f"{title} tagline",
            description=f"{title} description",
            category=category,
            github_url=f"https://github.com/dim-gggl/{slug}",
            completed_at="2024-01-01",
            is_published=is_published,
            order=order,
        )
        if technologies:
            project.technologies.set(technologies)
        return project

    def test_home_page(self, client):
        response = client.get(reverse("core:home"), secure=True)

        assert response.status_code == 200
        assert "Dimitri" in response.content.decode()

    def test_home_page_exposes_navigation_context(self, client):
        response = client.get(reverse("core:home"), secure=True)

        assert response.status_code == 200
        assert "home_intro" in response.context
        assert "navigation_sections" in response.context
        assert len(response.context["navigation_sections"]) == 5

    def test_home_page_renders_navigation_links(self, client):
        response = client.get(reverse("core:home"), secure=True)
        content = response.content.decode()

        assert response.status_code == 200
        assert reverse("core:ai") in content
        assert reverse("core:cli") in content
        assert reverse("core:django") in content
        assert reverse("projects:list") in content
        assert reverse("core:about") in content

    def test_ai_page_returns_200_and_exposes_context(self, client):
        category = self._make_category("AI", "ai")
        python = self._make_technology("Python", "python", "language")

        self._make_project("sunoreverse", "sunoreverse", category, [python], order=1)
        self._make_project("suno-arch", "suno-arch", category, [python], order=2)
        self._make_project("market-pal", "market-pal", category, [python], order=3)
        self._make_project("KinoLOG", "KinoLOG", category, [python], order=4)

        response = client.get(reverse("core:ai"), secure=True)

        assert response.status_code == 200
        assert "ai_page" in response.context
        assert "vibe_projects" in response.context
        assert [project.slug for project in response.context["vibe_projects"]] == [
            "sunoreverse",
            "suno-arch",
            "market-pal",
            "KinoLOG",
        ]

    def test_cli_page_returns_curated_published_projects_only(self, client):
        category = self._make_category("CLI", "cli")
        python = self._make_technology("Python", "python", "language")

        self._make_project("Epic Events", "epic_events", category, [python], order=1)
        self._make_project(
            "AlgoInvest&Trade",
            "AlgoInvest-Trade",
            category,
            [python],
            order=2,
        )
        self._make_project("ChessUp", "Chess_Up", category, [python], order=3)
        self._make_project(
            "Book Scraper",
            "Book_Scraper",
            category,
            [python],
            order=4,
        )
        self._make_project("clinkey-cli", "clinkey-cli", category, [python], order=5)
        self._make_project(
            "Hidden CLI",
            "hidden-cli",
            category,
            [python],
            is_published=False,
            order=6,
        )

        response = client.get(reverse("core:cli"), secure=True)

        assert response.status_code == 200
        assert [project.slug for project in response.context["projects"]] == [
            "epic_events",
            "AlgoInvest-Trade",
            "Chess_Up",
            "Book_Scraper",
            "clinkey-cli",
        ]

    def test_django_page_selects_django_and_drf_projects(self, client):
        category = self._make_category("Web", "web")
        django = self._make_technology("Django", "django", "backend")
        drf = self._make_technology(
            "Django Rest Framework",
            "django-rest-framework",
            "backend",
        )
        python = self._make_technology("Python", "python", "language")

        django_only = self._make_project(
            "LITReview",
            "lit_review",
            category,
            [django],
            order=1,
        )
        drf_project = self._make_project(
            "SoftDesk Support",
            "softdesk_support",
            category,
            [django, drf],
            order=2,
        )
        self._make_project(
            "Python CLI",
            "python-cli",
            category,
            [python],
            order=3,
        )
        self._make_project(
            "Hidden DRF",
            "hidden-drf",
            category,
            [drf],
            is_published=False,
            order=4,
        )

        response = client.get(reverse("core:django"), secure=True)

        assert response.status_code == 200
        assert response.context["projects"][0] == django_only
        assert response.context["projects"][1] == drf_project
        assert [project.slug for project in response.context["projects"]] == [
            "lit_review",
            "softdesk_support",
        ]

    def test_about_page(self, client):
        response = client.get(reverse("core:about"), secure=True)
        assert response.status_code == 200

    def test_skills_page(self, client):
        response = client.get(reverse("core:skills"), secure=True)
        assert response.status_code == 200

    def test_navbar_uses_canonical_labels(self, client):
        response = client.get(reverse("core:home"), secure=True)
        content = response.content.decode()

        assert "HOME" in content
        assert "IA" in content
        assert "CLI" in content
        assert "DJANGO" in content
        assert "PROJETS" in content
        assert "A PROPOS" in content

    def test_navbar_marks_current_page(self, client):
        response = client.get(reverse("core:ai"), secure=True)
        content = response.content.decode()

        assert 'aria-current="page"' in content
