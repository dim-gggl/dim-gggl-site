import pytest

from portfolio_dimitri import settings as project_settings


@pytest.mark.parametrize(
    ("raw_debug", "environment", "expected"),
    [
        (None, "development", True),
        ("False", "development", False),
        (None, "production", False),
    ],
)
def test_resolve_debug_uses_safe_defaults(raw_debug, environment, expected):
    assert project_settings._resolve_debug(raw_debug, environment) is expected


def test_debug_uses_non_manifest_staticfiles_storage():
    assert project_settings.DEBUG is True
    assert project_settings.STORAGES["staticfiles"]["BACKEND"] == (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
