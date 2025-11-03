"""
Management command to import gallery images from local static/images directory.
Creates ProjectImage objects for each project using existing local files.

Usage:
    python manage.py import_local_gallery_images
"""

import os
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from projects.models import Project, ProjectImage


class Command(BaseCommand):
    help = "Import gallery images from local static/images directory"

    # Mapping of project slugs to their local gallery images
    LOCAL_GALLERY_IMAGES = {
        "epic_events": [
            {
                "filename": "epic-events-help.png",
                "caption": "Panneau d'aide de l'interface CLI",
                "order": 1,
            },
        ],
        "Clinkey": [
            {
                "filename": "ClinKey_light.png",
                "caption": "Interface avec thème clair",
                "order": 1,
            },
            {
                "filename": "ClinKey_dark.png",
                "caption": "Interface avec thème sombre",
                "order": 2,
            },
        ],
        # Add more mappings as you create/add gallery images to static/images/
        # Format:
        # "project_slug": [
        #     {
        #         "filename": "image_name.png",
        #         "caption": "Image description",
        #         "order": 1,
        #     },
        # ],
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

        self.stdout.write(self.style.SUCCESS("Starting local gallery images import..."))

        if dry_run:
            self.stdout.write(
                self.style.WARNING("DRY RUN MODE - No objects will be created")
            )

        # Path to static images directory
        static_images_dir = Path(settings.BASE_DIR) / "static" / "images"

        if not static_images_dir.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Static images directory not found: {static_images_dir}"
                )
            )
            return

        total_created = 0
        total_skipped = 0
        total_errors = 0

        for project_slug, images in self.LOCAL_GALLERY_IMAGES.items():
            try:
                project = Project.objects.get(slug=project_slug)
                self.stdout.write(
                    f"\nProcessing project: {project.title} ({project_slug})"
                )

                if force and not dry_run:
                    deleted_count = project.gallery_images.all().delete()[0]
                    if deleted_count > 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f"  Deleted {deleted_count} existing gallery images"
                            )
                        )

                for image_data in images:
                    filename = image_data["filename"]
                    caption = image_data["caption"]
                    order = image_data["order"]

                    # Check if image file exists
                    image_path = static_images_dir / filename

                    if not image_path.exists():
                        self.stdout.write(
                            self.style.ERROR(f"  ✗ Image file not found: {filename}")
                        )
                        total_errors += 1
                        continue

                    # Check if gallery image already exists
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
                            self.style.NOTICE(
                                f"  [DRY RUN] Would import: {filename} - {caption}"
                            )
                        )
                        total_created += 1
                        continue

                    # Create ProjectImage object
                    try:
                        with open(image_path, "rb") as img_file:
                            gallery_image = ProjectImage(
                                project=project,
                                caption=caption,
                                order=order,
                            )
                            gallery_image.image.save(
                                filename,
                                File(img_file),
                                save=True,
                            )

                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ Created: {caption} ({filename})")
                        )
                        total_created += 1

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
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Import complete! You can add more gallery images via the Django admin."
                )
            )
