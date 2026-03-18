"""
Tests for site-wide language selection and translated UI rendering.
"""

from __future__ import annotations

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
class TestLocalization:
    def test_should_render_english_navigation_by_default(self, client):
        """
        Ensure the default locale renders the navigation in English.
        """

        response = client.get(reverse("core:home"))

        assert response.status_code == 200
        content = response.content.decode()

        assert 'lang="en"' in content
        assert "Projects" in content
        assert "About" in content
        assert "FR" in content

    def test_should_switch_to_french_via_language_endpoint(self, client):
        """
        Ensure the language switch stores the French locale and updates the UI.
        """

        response = client.post(
            reverse("set_language"),
            data={"language": "fr", "next": reverse("core:home")},
        )

        assert response.status_code == 302
        assert response.cookies[settings.LANGUAGE_COOKIE_NAME].value == "fr"

        localized_response = client.get(reverse("core:home"))

        assert localized_response.status_code == 200
        content = localized_response.content.decode()

        assert 'lang="fr"' in content
        assert "Projets" in content
        assert "À propos" in content
        assert "EN" in content

