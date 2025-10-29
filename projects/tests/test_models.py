import pytest
from projects.models import Project


@pytest.mark.django_db
class TestProjectModel:
    def test_project_creation(self):
        """Project slug should be generated automatically from title."""
        project = Project.objects.create(
            title="Test Project",
            tagline="Test tagline",
            description="Test description",
            completed_at="2024-01-01",
        )
        assert project.slug == "test-project"
        assert str(project) == "Test Project"

    def test_project_gradient_css(self):
        """Gradient CSS string should include linear-gradient and colors."""
        project = Project.objects.create(
            title="Test",
            tagline="tag",
            description="desc",
            primary_color="#ff0000",
            secondary_color="#00ff00",
            completed_at="2024-01-01",
        )
        assert "linear-gradient" in project.gradient_css
        assert "#ff0000" in project.gradient_css

    def test_get_similar_projects(self):
        """Similar projects should share technologies with the current project."""
        p1 = Project.objects.create(
            title="P1",
            tagline="t1",
            description="d1",
            completed_at="2024-01-01",
        )
        p2 = Project.objects.create(
            title="P2",
            tagline="t2",
            description="d2",
            completed_at="2024-01-02",
        )
        # Without technologies set, similar list should be empty
        assert list(p1.get_similar_projects()) == []

