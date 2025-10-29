import pytest
from django.urls import reverse
from projects.models import Project


@pytest.mark.django_db
class TestProjectViews:
    def test_project_list_view(self, client):
        """Project list view renders and exposes 'projects' in context."""
        response = client.get(reverse("projects:list"))
        assert response.status_code == 200
        assert "projects" in response.context

    def test_project_detail_view(self, client):
        """Detail view returns 200 and includes the project in context."""
        project = Project.objects.create(
            title="Detail Project",
            tagline="Tag",
            description="Desc",
            completed_at="2024-01-01",
        )
        url = reverse("projects:detail", kwargs={"slug": project.slug})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context["project"] == project

    def test_project_filtering_by_technology(self, client):
        """Filtering by technology slug returns 200 even without data."""
        response = client.get(reverse("projects:list") + "?tech=python")
        assert response.status_code == 200

