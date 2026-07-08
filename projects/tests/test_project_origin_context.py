"""
Tests for the origin context returned by the project detail API.

The frontend appends ``?from=<origin>`` when navigating from the curated
AI / CLI / Django pages; the API answers with a localized back link.
"""

import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProjectOriginContext:
    @pytest.mark.parametrize(
        ("origin", "label", "url"),
        [
            ("ai", "Back to AI", "/ai/"),
            ("cli", "Back to CLI", "/cli/"),
            ("django", "Back to Django", "/django/"),
        ],
    )
    def test_detail_returns_origin_context(
        self, client, project_factory, origin, label, url
    ):
        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
            + f"?from={origin}"
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["origin_context"] == {"label": label, "url": url}

    def test_detail_translates_origin_label(self, client, project_factory):
        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
            + "?from=ai&lang=fr"
        )

        data = json.loads(response.content)
        assert data["origin_context"]["label"] == "Retour vers IA"

    def test_detail_ignores_unknown_origin(self, client, project_factory):
        project = project_factory()

        response = client.get(
            reverse("api:project-detail", kwargs={"slug": project.slug})
            + "?from=unknown"
        )

        data = json.loads(response.content)
        assert data["origin_context"] is None
