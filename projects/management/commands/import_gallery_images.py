"""
Management command to import gallery images from the old portfolio.
Downloads images and creates ProjectImage objects for each project.

Usage:
    python manage.py import_gallery_images
"""

import os
from io import BytesIO

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from projects.models import Project, ProjectImage


class Command(BaseCommand):
    help = "Import gallery images from old portfolio GitHub Pages"

    # Mapping of project slugs to their gallery images (from old portfolio)
    GALLERY_IMAGES = {
        "epic_events": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/epic_events_help.svg",
                "caption": "Panneau d'aide de l'interface CLI",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/epic_events_details.svg",
                "caption": "Affichage détaillé d'un client",
                "order": 2,
            },
        ],
        "softdesk_support": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/softdesk_user_detail.png",
                "caption": "Endpoint User Detail - Données utilisateur",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/softdesk_user_list.png",
                "caption": "Endpoint User List - Liste paginée",
                "order": 2,
            },
        ],
        "Chess_Up": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/chess_up_menu.png",
                "caption": "Menu principal du gestionnaire de tournois",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/chess_up_results.png",
                "caption": "Affichage des résultats d'une ronde",
                "order": 2,
            },
        ],
        "Book_Scraper": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/book_scraper_menu.png",
                "caption": "Menu d'interaction du terminal",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/book_scraper_csv.png",
                "caption": "Exemple de données CSV extraites",
                "order": 2,
            },
        ],
        "clinkey-cli": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/clinkey_cli_welcome.png",
                "caption": "Écran d'accueil du mode interactif",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/clinkey_cli_output.png",
                "caption": "Affichage des mots de passe générés",
                "order": 2,
            },
        ],
        "Clinkey": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/clinkey_light_theme.png",
                "caption": "Interface avec thème clair",
                "order": 1,
            },
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/clinkey_dark_theme.png",
                "caption": "Interface avec thème sombre",
                "order": 2,
            },
        ],
        "aura-app": [
            {
                "url": "https://dim-gggl.github.io/portfolio/assets/images/aura_home_mobile.png",
                "caption": "Page d'accueil optimisée mobile",
                "order": 1,
            },
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate the import without creating objects",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete existing gallery images before importing",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        force = options["force"]

        self.stdout.write(
            self.style.SUCCESS("Starting gallery images import from old portfolio...")
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No objects will be created")
            )

        total_created = 0
        total_skipped = 0
        total_errors = 0

        for project_slug, images in self.GALLERY_IMAGES.items():
            try:
                project = Project.objects.get(slug=project_slug)
                self.stdout.write(f"\nProcessing project: {project.title} ({project_slug})")

                if force and not dry_run:
                    deleted_count = project.gallery_images.all().delete()[0]
                    if deleted_count > 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  Deleted {deleted_count} existing gallery images"
                            )
                        )

                for image_data in images:
                    url = image_data["url"]
                    caption = image_data["caption"]
                    order = image_data["order"]

                    # Check if image already exists
                    existing = project.gallery_images.filter(
                        caption=caption, order=order
                    ).first()

                    if existing and not force:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ⊘ Skipped: {caption} (already exists)"
                            )
                        )
                        total_skipped += 1
                        continue

                    if dry_run:
                        self.stdout.write(
                            self.style.NOTICE(f"  [DRY RUN] Would download: {caption}")
                        )
                        total_created += 1
                        continue

                    # Download the image
                    try:
                        self.stdout.write(f"  Downloading: {url}")
                        response = requests.get(url, timeout=10)
                        response.raise_for_status()

                        # Extract filename from URL
                        filename = os.path.basename(url)

                        # Create ProjectImage object
                        gallery_image = ProjectImage(
                            project=project,
                            caption=caption,
                            order=order,
                        )

                        # Save the downloaded image
                        gallery_image.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True,
                        )

                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Created: {caption}")
                        )
                        total_created += 1

                    except requests.RequestException as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ✗ Failed to download {url}: {str(e)}"
                            )
                        )
                        total_errors += 1
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"  ✗ Error creating gallery image: {str(e)}"
                            )
                        )
                        total_errors += 1

            except Project.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Project not found: {project_slug} - Run load_projects first"
                    )
                )
                total_errors += 1
                continue

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("\nImport Summary:"))
        self.stdout.write(f"  Created: {total_created}")
        self.stdout.write(f"  Skipped: {total_skipped}")
        self.stdout.write(f"  Errors:  {total_errors}")
        self.stdout.write("=" * 60)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "\nThis was a DRY RUN. Run without --dry-run to actually import."
                )
            )
