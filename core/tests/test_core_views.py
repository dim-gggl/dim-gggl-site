import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCoreViews:
    def test_home_page(self, client):
        response = client.get(reverse("core:home"))
        assert response.status_code == 200
        assert "Dimitri" in response.content.decode()

    def test_about_page(self, client):
        response = client.get(reverse("core:about"))
        assert response.status_code == 200

    def test_skills_page(self, client):
        response = client.get(reverse("core:skills"))
        assert response.status_code == 200
