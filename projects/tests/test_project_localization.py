"""
Tests for translated project content rendering.
"""
from html import unescape

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
class TestProjectLocalization:
    def test_should_render_project_content_in_french_when_locale_is_french(
        self,
        client,
        project_factory,
    ):
        """
        Ensure dynamic project fields are translated when French is active.
        """

        project = project_factory()
        client.cookies[settings.LANGUAGE_COOKIE_NAME] = "fr"

        response = client.get(
            reverse("projects:detail", kwargs={"slug": project.slug})
        )

        assert response.status_code == 200
        content = unescape(response.content.decode())

        assert "Projets d'étude" in content
        assert "CRM CLI pour une agence événementielle" in content
        assert "Authentification JWT (SimpleJWT)" in content
