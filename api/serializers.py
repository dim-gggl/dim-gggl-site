"""
JSON serialization helpers for the portfolio API.

The React frontend consumes these payloads. All user-facing content is
localized server-side through the existing translation catalog so the
frontend never needs to know about the source language.
"""

from __future__ import annotations

from core.localization.translation_service import translate_text


def serialize_technology(tech, language=None):
    """Serialize a Technology for badges and stack grids."""
    return {
        "name": tech.name,
        "slug": tech.slug,
        "category": tech.category,
        "category_label": translate_text(
            tech.get_category_display(), language
        ),
        "color": tech.color,
        "proficiency": tech.proficiency,
    }


def serialize_category(category, language=None):
    """Serialize a Category, including its translated name."""
    if category is None:
        return None
    return {
        "name": translate_text(category.name, language),
        "slug": category.slug,
    }


def serialize_project_card(project, language=None):
    """Serialize the fields needed to render a project card."""
    return {
        "slug": project.slug,
        "title": project.title,
        "tagline": translate_text(project.tagline, language),
        "category": serialize_category(project.category, language),
        "technologies": [
            serialize_technology(tech, language)
            for tech in project.technologies.all()
        ],
        "primary_color": project.primary_color,
        "secondary_color": project.secondary_color,
        "card_image": project.get_card_image_url(),
        "featured_image": (
            project.featured_image.url if project.featured_image else ""
        ),
        "github_url": project.github_url,
        "demo_url": project.demo_url,
        "completed_at": (
            project.completed_at.isoformat() if project.completed_at else None
        ),
        "url": f"/projects/{project.slug}/",
    }


def serialize_project_detail(project, language=None):
    """Serialize the full project payload for the detail page."""
    data = serialize_project_card(project, language)
    gallery = [
        {
            "url": image.image.url,
            "caption": image.caption,
        }
        for image in project.gallery_images.all()
    ] + [
        {
            "url": image["url"],
            "caption": "",
        }
        for image in project.get_gallery_images()
    ]
    data.update(
        {
            "description": translate_text(project.description, language),
            "challenges": translate_text(project.challenges, language),
            "learnings": translate_text(project.learnings, language),
            "features": [
                translate_text(feature, language)
                for feature in (project.features or [])
            ],
            "documentation_url": project.documentation_url,
            "duration": project.duration,
            "logo": project.logo.url if project.logo else "",
            "gallery": gallery,
        }
    )
    return data
