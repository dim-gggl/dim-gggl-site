import json
from pathlib import Path


PROJECTS_JSON_PATH = Path(__file__).resolve().parents[2] / "projects.json"


def load_projects():
    return json.loads(PROJECTS_JSON_PATH.read_text(encoding="utf-8"))


def test_projects_json_has_unique_slugs():
    projects = load_projects()
    slugs = [project["slug"] for project in projects]

    assert len(slugs) == len(set(slugs))


def test_projects_json_contains_required_ai_projects_as_published():
    projects = load_projects()
    projects_by_slug = {project["slug"]: project for project in projects}

    required_ai_slugs = [
        "sunoreverse",
        "suno-arch",
        "market-pal",
        "KinoLOG",
    ]

    for slug in required_ai_slugs:
        assert slug in projects_by_slug
        assert projects_by_slug[slug]["is_published"] is True


def test_projects_json_contains_first_release_cli_slugs():
    projects = load_projects()
    slugs = {project["slug"] for project in projects}

    expected_cli_slugs = {
        "epic_events",
        "AlgoInvest-Trade",
        "Chess_Up",
        "Book_Scraper",
        "clinkey-cli",
    }

    assert expected_cli_slugs.issubset(slugs)
