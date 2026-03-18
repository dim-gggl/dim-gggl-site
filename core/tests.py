from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class HomeViewTests(TestCase):
    def test_homepage_injects_four_random_featured_projects(self):
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

        response = self.client.get(reverse("core:home"))
        featured_projects = response.context["featured_projects"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(featured_projects), 4)
        self.assertTrue(all(project.is_featured for project in featured_projects))
        self.assertTrue(all(project.is_published for project in featured_projects))
