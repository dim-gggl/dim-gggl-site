"""
Tests for translated project content in the API payloads.
"""

import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProjectLocalization:
    def test_should_return_french_content_when_lang_is_french(
        self,
        client,
        project_factory,
    ):
        """Ensure dynamic project fields are translated for ?lang=fr."""

        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
            + "?lang=fr"
        )

        assert response.status_code == 200
        data = json.loads(response.content)

        assert data["category"]["name"] == "Projets d'étude"
        assert data["tagline"] == "CRM CLI pour une agence événementielle"
        assert "Authentification JWT (SimpleJWT)" in data["features"]

    def test_should_return_english_content_by_default(
        self,
        client,
        project_factory,
    ):
        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
        )

        data = json.loads(response.content)
        assert data["tagline"] == "CLI CRM for an event agency"
