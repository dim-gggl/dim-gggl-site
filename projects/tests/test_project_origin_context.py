import pytest
from django.urls import reverse

from projects.models import Category, Project, Technology


@pytest.fixture(autouse=True)
def project_origin_test_settings(settings):
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
class TestProjectOriginContext:
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

    def _make_project(self, title, slug, category, technologies=None, order=0):
        project = Project.objects.create(
            title=title,
            slug=slug,
            tagline=f"{title} tagline",
            description=f"{title} description",
            category=category,
            github_url=f"https://github.com/dim-gggl/{slug}",
            completed_at="2024-01-01",
            is_published=True,
            order=order,
        )
        if technologies:
            project.technologies.set(technologies)
        return project

    def test_ai_page_appends_ai_origin_to_project_links(self, client):
        category = self._make_category("AI", "ai")
        python = self._make_technology("Python", "python", "language")

        self._make_project("sunoreverse", "sunoreverse", category, [python], order=1)
        self._make_project("suno-arch", "suno-arch", category, [python], order=2)
        self._make_project("market-pal", "market-pal", category, [python], order=3)
        self._make_project("KinoLOG", "KinoLOG", category, [python], order=4)

        response = client.get(reverse("core:ai"), secure=True)
        content = response.content.decode()

        assert f'{reverse("projects:detail", kwargs={"slug": "sunoreverse"})}?from=ai' in content

    def test_cli_page_appends_cli_origin_to_project_links(self, client):
        category = self._make_category("CLI", "cli")
        python = self._make_technology("Python", "python", "language")

        self._make_project("Epic Events", "epic_events", category, [python], order=1)
        self._make_project("AlgoInvest", "AlgoInvest-Trade", category, [python], order=2)
        self._make_project("ChessUp", "Chess_Up", category, [python], order=3)
        self._make_project("Book Scraper", "Book_Scraper", category, [python], order=4)
        self._make_project("clinkey-cli", "clinkey-cli", category, [python], order=5)

        response = client.get(reverse("core:cli"), secure=True)
        content = response.content.decode()

        assert f'{reverse("projects:detail", kwargs={"slug": "epic_events"})}?from=cli' in content

    def test_django_page_appends_django_origin_to_project_links(self, client):
        category = self._make_category("Web", "web")
        django = self._make_technology("Django", "django", "backend")

        self._make_project("LITReview", "lit_review", category, [django], order=1)

        response = client.get(reverse("core:django"), secure=True)
        content = response.content.decode()

        assert f'{reverse("projects:detail", kwargs={"slug": "lit_review"})}?from=django' in content

    def test_project_detail_shows_contextual_back_link_for_valid_origin(self, client):
        category = self._make_category("AI", "ai")
        python = self._make_technology("Python", "python", "language")
        project = self._make_project("sunoreverse", "sunoreverse", category, [python], order=1)

        response = client.get(
            f'{reverse("projects:detail", kwargs={"slug": project.slug})}?from=ai',
            secure=True,
        )
        content = response.content.decode()

        assert reverse("core:ai") in content
        assert "Retour vers IA" in content

    def test_project_detail_hides_contextual_back_link_for_invalid_origin(self, client):
        category = self._make_category("AI", "ai")
        python = self._make_technology("Python", "python", "language")
        project = self._make_project("sunoreverse", "sunoreverse", category, [python], order=1)

        response = client.get(
            f'{reverse("projects:detail", kwargs={"slug": project.slug})}?from=unknown',
            secure=True,
        )
        content = response.content.decode()

        assert "Retour vers IA" not in content
        assert "Retour vers CLI" not in content
        assert "Retour vers DJANGO" not in content

    def test_project_detail_previous_and_next_links_do_not_propagate_origin(self, client):
        category = self._make_category("AI", "ai")
        python = self._make_technology("Python", "python", "language")
        first = self._make_project("first", "first-project", category, [python], order=1)
        current = self._make_project("current", "current-project", category, [python], order=2)
        self._make_project("third", "third-project", category, [python], order=3)

        response = client.get(
            f'{reverse("projects:detail", kwargs={"slug": current.slug})}?from=ai',
            secure=True,
        )
        content = response.content.decode()

        assert f'href="{reverse("projects:detail", kwargs={"slug": first.slug})}"' in content
        assert "?from=ai" not in content.split("Previous project")[1]
