import json

import pytest
from django.urls import reverse

from projects.models import Category, Project, Technology


@pytest.fixture(autouse=True)
def core_view_test_settings(settings):
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }


def make_category(name, slug):
    return Category.objects.create(
        name=name,
        slug=slug,
        description=f"{name} category",
    )


def make_technology(name, slug, category):
    return Technology.objects.create(name=name, slug=slug, category=category)


def make_project(
    title,
    slug,
    category,
    technologies=None,
    is_published=True,
    is_featured=False,
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
        is_featured=is_featured,
        order=order,
    )
    if technologies:
        project.technologies.set(technologies)
    return project


@pytest.mark.django_db
class TestSpaViews:
    """Every page route serves the React SPA shell."""

    @pytest.mark.parametrize(
        "url_name",
        [
            "core:home",
            "core:ai",
            "core:cli",
            "core:django",
            "core:about",
            "core:skills",
        ],
    )
    def test_page_serves_spa_shell(self, client, url_name):
        response = client.get(reverse(url_name), secure=True)

        assert response.status_code == 200
        content = response.content.decode()
        assert 'id="root"' in content
        assert "frontend/assets/app.js" in content


@pytest.mark.django_db
class TestSiteApi:
    def test_site_payload_exposes_person_ui_and_stats(self, client):
        response = client.get(reverse("api:site"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["person"]["name"] == "Dimitri Gaggioli"
        assert data["languages"] == ["en", "fr"]
        assert data["ui"]["nav.home"] == "Home"
        assert "projects" in data["stats"]

    def test_site_payload_localizes_ui_catalog(self, client):
        response = client.get(reverse("api:site") + "?lang=fr", secure=True)

        data = json.loads(response.content)
        assert data["language"] == "fr"
        assert data["ui"]["nav.home"] == "Accueil"


@pytest.mark.django_db
class TestHomeApi:
    def test_home_exposes_intro_and_navigation(self, client):
        response = client.get(reverse("api:home"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["intro"]["title"] == "dim-gggl"
        assert len(data["navigation"]) == 5
        assert [section["url"] for section in data["navigation"]] == [
            "/ai/",
            "/cli/",
            "/django/",
            "/projects/",
            "/about/",
        ]

    def test_home_returns_featured_projects_only(self, client):
        category = make_category("Web", "web")
        make_project("Featured", "featured", category, is_featured=True)
        make_project("Regular", "regular", category, is_featured=False)

        response = client.get(reverse("api:home"), secure=True)

        data = json.loads(response.content)
        assert [
            project["slug"] for project in data["featured"]
        ] == ["featured"]


@pytest.mark.django_db
class TestAiApi:
    def test_ai_payload_exposes_prompting_and_curated_projects(self, client):
        category = make_category("AI", "ai")
        python = make_technology("Python", "python", "language")

        make_project("sunoreverse", "sunoreverse", category, [python], order=1)
        make_project("suno-arch", "suno-arch", category, [python], order=2)
        make_project("market-pal", "market-pal", category, [python], order=3)
        make_project("KinoLOG", "KinoLOG", category, [python], order=4)

        response = client.get(reverse("api:ai"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["prompting"]["intro"]["title"] == "Prompting"
        assert data["prompting"]["music"]["track_title"] == "Un mot"
        assert data["prompting"]["video"]["sora_url"].startswith(
            "https://sora"
        )
        assert [
            project["slug"] for project in data["vibe_engineering"]["projects"]
        ] == ["sunoreverse", "suno-arch", "market-pal", "KinoLOG"]


@pytest.mark.django_db
class TestCliApi:
    def test_cli_returns_curated_published_projects_only(self, client):
        category = make_category("CLI", "cli")
        python = make_technology("Python", "python", "language")

        make_project("Epic Events", "epic_events", category, [python], order=1)
        make_project(
            "AlgoInvest&Trade", "AlgoInvest-Trade", category, [python], order=2
        )
        make_project("ChessUp", "Chess_Up", category, [python], order=3)
        make_project(
            "Book Scraper", "Book_Scraper", category, [python], order=4
        )
        make_project("clinkey-cli", "clinkey-cli", category, [python], order=5)
        make_project(
            "Hidden CLI",
            "hidden-cli",
            category,
            [python],
            is_published=False,
            order=6,
        )

        response = client.get(reverse("api:cli"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert [project["slug"] for project in data["projects"]] == [
            "epic_events",
            "AlgoInvest-Trade",
            "Chess_Up",
            "Book_Scraper",
            "clinkey-cli",
        ]


@pytest.mark.django_db
class TestDjangoApi:
    def test_django_selects_django_and_drf_projects(self, client):
        category = make_category("Web", "web")
        django = make_technology("Django", "django", "backend")
        drf = make_technology(
            "Django Rest Framework", "django-rest-framework", "backend"
        )
        python = make_technology("Python", "python", "language")

        make_project("LITReview", "lit_review", category, [django], order=1)
        make_project(
            "SoftDesk Support",
            "softdesk_support",
            category,
            [django, drf],
            order=2,
        )
        make_project("Python CLI", "python-cli", category, [python], order=3)
        make_project(
            "Hidden DRF",
            "hidden-drf",
            category,
            [drf],
            is_published=False,
            order=4,
        )

        response = client.get(reverse("api:django"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert [project["slug"] for project in data["projects"]] == [
            "lit_review",
            "softdesk_support",
        ]


@pytest.mark.django_db
class TestAboutApi:
    def test_about_groups_technologies_by_category(self, client):
        make_technology("Python", "python", "language")
        make_technology("PostgreSQL", "postgresql", "database")
        make_technology("Docker", "docker", "tool")
        make_technology("React", "react", "frontend")

        response = client.get(reverse("api:about"), secure=True)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert [
            tech["name"] for tech in data["skills"]["backend"]
        ] == ["Python"]
        assert [tech["name"] for tech in data["skills"]["database"]] == [
            "PostgreSQL"
        ]
        assert [tech["name"] for tech in data["skills"]["tools"]] == ["Docker"]
        assert [
            tech["name"] for tech in data["skills"]["frontend"]
        ] == ["React"]
        assert data["skills"]["backend"][0]["color_from"]
