import json

import pytest
from django.urls import reverse

from projects.models import Project


@pytest.mark.django_db
class TestProjectSpaViews:
    def test_project_list_serves_spa_shell(self, client):
        response = client.get(reverse("projects:list"))
        assert response.status_code == 200
        assert 'id="root"' in response.content.decode()

    def test_project_detail_serves_spa_shell(self, client):
        project = Project.objects.create(
            title="Detail Project",
            tagline="Tag",
            description="Desc",
            completed_at="2024-01-01",
        )
        url = reverse("projects:detail", kwargs={"slug": project.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert 'id="root"' in response.content.decode()


@pytest.mark.django_db
class TestProjectListApi:
    def test_list_returns_published_projects(self, client, project_factory):
        project = project_factory()
        project_factory(is_published=False)

        response = client.get(reverse("api:project-list"))

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["filtered_count"] == 1
        assert data["results"][0]["slug"] == project.slug
        assert "technologies" in data
        assert "categories" in data

    def test_list_filters_by_search(self, client, project_factory):
        match = project_factory(title="Clinkey", slug="clinkey")
        project_factory(title="Other", slug="other")

        response = client.get(reverse("api:project-list") + "?q=clinkey")

        data = json.loads(response.content)
        assert [item["slug"] for item in data["results"]] == [match.slug]

    def test_list_filters_by_technology_without_data(self, client):
        response = client.get(reverse("api:project-list") + "?tech=python")
        assert response.status_code == 200
        assert json.loads(response.content)["results"] == []

    def test_list_sorts_by_title(self, client, project_factory):
        project_factory(title="Zeta", slug="zeta")
        project_factory(title="Alpha", slug="alpha")

        response = client.get(reverse("api:project-list") + "?sort=title")

        data = json.loads(response.content)
        assert [item["title"] for item in data["results"]] == ["Alpha", "Zeta"]


@pytest.mark.django_db
class TestProjectDetailApi:
    def test_detail_returns_full_payload(self, client, project_factory):
        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["slug"] == project.slug
        assert data["description"]
        assert isinstance(data["features"], list)
        assert "similar" in data
        assert "previous" in data
        assert "next" in data

    def test_detail_returns_404_for_unpublished(self, client, project_factory):
        project = project_factory(is_published=False)

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
        )

        assert response.status_code == 404

    def test_detail_links_previous_and_next(self, client, project_factory):
        first = project_factory(order=1)
        second = project_factory(order=2)
        third = project_factory(order=3)

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": second.slug})
        )

        data = json.loads(response.content)
        assert data["previous"]["slug"] == first.slug
        assert data["next"]["slug"] == third.slug
