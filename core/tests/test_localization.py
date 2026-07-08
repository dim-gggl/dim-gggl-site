"""
Tests for site-wide language selection.

The UI itself is localized client-side by the React app, which pulls
its strings from the ``/api/site/`` catalog; these tests cover the
server-side pieces: the shell's lang attribute, the historical
``set_language`` endpoint, and the localized API catalog.
"""

from __future__ import annotations

import json

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
class TestLocalization:
    def test_should_serve_english_shell_and_catalog_by_default(self, client):
        response = client.get(reverse("core:home"))

        assert response.status_code == 200
        assert 'lang="en"' in response.content.decode()

        api_response = client.get(reverse("api:site"))
        data = json.loads(api_response.content)
        assert data["ui"]["nav.projects"] == "Projects"
        assert data["ui"]["nav.about"] == "About"

    def test_should_switch_to_french_via_language_endpoint(self, client):
        response = client.post(
            reverse("set_language"),
            data={"language": "fr", "next": reverse("core:home")},
        )

        assert response.status_code == 302
        assert response.cookies[settings.LANGUAGE_COOKIE_NAME].value == "fr"

        localized_response = client.get(reverse("core:home"))
        assert localized_response.status_code == 200
        assert 'lang="fr"' in localized_response.content.decode()

        api_response = client.get(reverse("api:site"))
        data = json.loads(api_response.content)
        assert data["language"] == "fr"
        assert data["ui"]["nav.projects"] == "Projets"
        assert data["ui"]["nav.about"] == "À propos"
