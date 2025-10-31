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

    def test_contact_page_get(self, client):
        response = client.get(reverse("core:contact"))
        assert response.status_code == 200
        assert "form" in response.context

    def test_contact_form_submission(self, client):
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "Test message with more than 20 characters to pass validation.",
        }
        response = client.post(reverse("core:contact"), data)
        assert response.status_code == 302
