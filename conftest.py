"""
Test fixtures shared across the Django project.

This module centralizes small factories used by localization tests so that
test data stays explicit, isolated, and easy to evolve.
"""

from __future__ import annotations

from collections.abc import Callable

import pytest

from projects.models import Category, Project


@pytest.fixture
def category_factory(db) -> Callable[..., Category]:
    """
    Build persisted project categories for tests.

    Returns:
        Callable[..., Category]: Factory creating Category instances with
        overridable attributes.
    """

    counter = 0

    def create_category(**overrides) -> Category:
        nonlocal counter
        counter += 1

        defaults = {
            "name": f"Study Projects {counter}",
            "slug": f"study-projects-{counter}",
            "description": "Study project category",
            "order": counter,
        }
        defaults.update(overrides)
        return Category.objects.create(**defaults)

    return create_category


@pytest.fixture
def project_factory(db, category_factory) -> Callable[..., Project]:
    """
    Build persisted projects for tests.

    Returns:
        Callable[..., Project]: Factory creating published Project instances
        with overridable attributes.
    """

    counter = 0

    def create_project(**overrides) -> Project:
        nonlocal counter
        counter += 1

        category = overrides.pop(
            "category",
            category_factory(
                name="Study Projects",
                slug="study-projects",
                description="Projects completed during training.",
            ),
        )

        defaults = {
            "title": f"Localized Project {counter}",
            "slug": f"localized-project-{counter}",
            "tagline": "CLI CRM for an event agency",
            "description": (
                "Manage your events, clients, contracts, and teammate profiles "
                "with an ergonomic, intuitive Command Line Interface."
            ),
            "challenges": (
                "Implemented the PostgreSQL database and secured the application "
                "with password hashing and JWT authentication."
            ),
            "learnings": "PostgreSQL, JWT, hashing, TUI",
            "features": [
                "JWT authentication (SimpleJWT)",
                "Project CRUD with contributor management",
            ],
            "completed_at": "2024-01-01",
            "is_published": True,
            "category": category,
        }
        defaults.update(overrides)
        return Project.objects.create(**defaults)

    return create_project

