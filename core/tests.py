import json

from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class HomeApiTests(TestCase):
    def test_home_api_returns_four_random_featured_projects(self):
        [
            Project.objects.create(
                title=f"Featured {index}",
                slug=f"featured-{index}",
                is_featured=True,
                is_published=True,
            )
            for index in range(5)
        ]
        Project.objects.create(
            title="Hidden featured",
            slug="hidden-featured",
            is_featured=True,
            is_published=False,
        )
        Project.objects.create(
            title="Regular project",
            slug="regular-project",
            is_featured=False,
            is_published=True,
        )

        response = self.client.get(reverse("api:home"))
        data = json.loads(response.content)
        featured_slugs = {project["slug"] for project in data["featured"]}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["featured"]), 4)
        self.assertNotIn("hidden-featured", featured_slugs)
        self.assertNotIn("regular-project", featured_slugs)
        self.assertTrue(
            featured_slugs <= {f"featured-{index}" for index in range(5)}
        )
