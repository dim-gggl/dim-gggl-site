import json
import os
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.text import slugify

from projects.models import Project, Technology, Category

class Command(BaseCommand):
    help = "Load projects from a JSON file into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file",
            type=str,
            help="Path to the JSON file containing the projects array",
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                projects_data = json.load(f)
        except FileNotFoundError as exc:
            raise CommandError(f"JSON file not found: {json_file}") from exc

        if not isinstance(projects_data, list):
            raise CommandError("JSON root must be an array of projects")

        tech_stack_path = Path(settings.BASE_DIR) / "tech_stack.json"
        if tech_stack_path.exists():
            try:
                with tech_stack_path.open("r", encoding="utf-8") as tech_file:
                    tech_stack = json.load(tech_file)
            except json.JSONDecodeError as exc:
                raise CommandError(
                    f"Invalid JSON format in tech stack file: {tech_stack_path}"
                ) from exc
            if not isinstance(tech_stack, dict):
                raise CommandError(
                    "tech_stack.json must contain an object mapping technology names to proficiency levels"
                )
        else:
            tech_stack = {}
            self.stdout.write(
                self.style.WARNING(
                    f"⚠ tech_stack.json not found at {tech_stack_path}. Default proficiency levels will be used."
                )
            )

        def get_proficiency(tech_name: str, default: int = 4) -> int:
            value = tech_stack.get(tech_name)
            if isinstance(value, (int, float)):
                try:
                    value_int = int(value)
                except (TypeError, ValueError):
                    return default
                if 1 <= value_int <= 5:
                    return value_int
            return default

        def generate_unique_slug(model_cls, base_slug: str, exclude_id=None) -> str:
            slug = base_slug or "item"
            index = 2
            qs = model_cls.objects.all()
            if exclude_id:
                qs = qs.exclude(id=exclude_id)
            while qs.filter(slug=slug).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            return slug

        # Ensure categories exist
        categories_by_name = {}
        for project_data in projects_data:
            cat_name = project_data.get("category", "Uncategorized")
            if cat_name not in categories_by_name:
                base_slug = slugify(cat_name) or "category"
                by_name = Category.objects.filter(name=cat_name).first()
                if by_name:
                    # Ensure slug uniqueness for existing record
                    by_name.slug = generate_unique_slug(
                        Category, base_slug, exclude_id=by_name.id
                    )
                    if not by_name.description:
                        by_name.description = f"Category {cat_name}"
                    if not by_name.color:
                        by_name.color = "#ff6b35"
                    if not by_name.icon:
                        by_name.icon = "📁"
                    by_name.save()
                    category, created = by_name, False
                else:
                    by_slug = Category.objects.filter(slug=base_slug).first()
                    if by_slug:
                        # Reuse slug holder, update name
                        by_slug.name = cat_name
                        if not by_slug.description:
                            by_slug.description = f"Category {cat_name}"
                        if not by_slug.color:
                            by_slug.color = "#ff6b35"
                        if not by_slug.icon:
                            by_slug.icon = "📁"
                        by_slug.save()
                        category, created = by_slug, False
                    else:
                        unique_slug = generate_unique_slug(Category, base_slug)
                        category = Category(
                            name=cat_name,
                            slug=unique_slug,
                            description=f"Category {cat_name}",
                            color="#ff6b35",
                            icon="📁",
                        )
                        category.save()
                        created = True
                categories_by_name[cat_name] = category
                if created:
                    self.stdout.write(f"✓ Created category: {cat_name}")

        # Ensure technologies exist
        all_tech_names = set()
        for project_data in projects_data:
            all_tech_names.update(project_data.get("technologies", []))

        tech_colors = {
            "Python": "#3776ab",
            "Django": "#0c4b33",
            "Flask": "#000000",
            "PostgreSQL": "#336791",
            "SQLite": "#003b57",
            "MySQL": "#4479a1",
            "JavaScript": "#f7df1e",
            "HTML": "#e34f26",
            "CSS": "#1572b6",
            "Git": "#f05032",
            "GitHub": "#181717",
            "JWT": "#000000",
            "Click": "#ff6b35",
            "Rich": "#f7931e",
            "Django Rest Framework": "#a30000",
            "Tailwind CSS": "#06b6d4",
            "Bootstrap": "#7952b3",
            "Jinja": "#b41717",
            "P.O.O.": "#3776ab",
            "CLI": "#4d4d4d",
            "M.V.C.": "#4d4d4d",
        }

        tech_categories = {
            "Python": "language",
            "JavaScript": "language",
            "HTML": "frontend",
            "CSS": "frontend",
            "Django": "backend",
            "Flask": "backend",
            "Django Rest Framework": "backend",
            "PostgreSQL": "database",
            "SQLite": "database",
            "MySQL": "database",
            "Git": "tool",
            "GitHub": "tool",
            "JWT": "backend",
            "Click": "backend",
            "Rich": "backend",
            "Tailwind CSS": "frontend",
            "Bootstrap": "frontend",
        }

        technologies_by_name = {}
        for tech_name in sorted(all_tech_names):
            base_slug = slugify(tech_name) or "tech"
            by_name = Technology.objects.filter(name=tech_name).first()
            if by_name:
                # Ensure slug uniqueness for this record
                by_name.slug = generate_unique_slug(
                    Technology, base_slug, exclude_id=by_name.id
                )
                by_name.category = tech_categories.get(tech_name, "tool")
                by_name.color = tech_colors.get(tech_name, "#ff6b35")
                by_name.icon = base_slug
                by_name.proficiency = get_proficiency(tech_name, by_name.proficiency or 4)
                by_name.save()
                tech, created = by_name, False
            else:
                by_slug = Technology.objects.filter(slug=base_slug).first()
                if by_slug:
                    # Reuse slug holder, update name
                    by_slug.name = tech_name
                    by_slug.category = tech_categories.get(tech_name, "tool")
                    by_slug.color = tech_colors.get(tech_name, "#ff6b35")
                    by_slug.icon = base_slug
                    by_slug.proficiency = get_proficiency(
                        tech_name, by_slug.proficiency or 4
                    )
                    by_slug.save()
                    tech, created = by_slug, False
                else:
                    unique_slug = generate_unique_slug(Technology, base_slug)
                    tech = Technology(
                        name=tech_name,
                        slug=unique_slug,
                        category=tech_categories.get(tech_name, "tool"),
                        color=tech_colors.get(tech_name, "#ff6b35"),
                        icon=base_slug,
                        proficiency=get_proficiency(tech_name),
                    )
                    tech.save()
                    created = True
            technologies_by_name[tech_name] = tech
            if created:
                self.stdout.write(f"✓ Created technology: {tech_name}")

        # Create or update projects
        created_count = 0
        updated_count = 0

        # Map slugs to featured images relative to MEDIA root
        image_mapping = {
            "aura-app": "images/aura_title.png",
            "clinkey-cli": "images/clinkey-cli-title.png",
            "softdesk_support": "images/softdesk-support-api.png",
            "epic_events": "images/epic-events-help.png",
        }

        featured_slugs = set(image_mapping.keys())

        for project_data in projects_data:
            tech_names = project_data.pop("technologies", [])
            category_name = project_data.pop("category", None)
            category = categories_by_name.get(category_name) if category_name else None

            # Provide a default completed_at if missing/empty
            completed_at = project_data.get("completed_at")
            if not completed_at:
                project_data["completed_at"] = date(2024, 1, 1)

            # Ensure fields exist for model
            # Unknown keys will be ignored by update_or_create via defaults unpack
            slug = project_data.get("slug")
            if not slug:
                raise CommandError("Each project must have a slug in the JSON data")

            # Attach featured image path if present on disk
            img_rel = image_mapping.get(slug)
            if img_rel:
                media_path = os.path.join(settings.MEDIA_ROOT, img_rel)
                if os.path.exists(media_path):
                    project_data["featured_image"] = img_rel
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠ Featured image not found on disk for {slug}: {media_path}"
                        )
                    )

            project, created = Project.objects.update_or_create(
                slug=slug,
                defaults={
                    **project_data,
                    "category": category,
                    "is_featured": slug in featured_slugs
                    or project_data.get("is_featured", False),
                },
            )

            # Set technologies (replace associations)
            project.technologies.clear()
            for tech_name in tech_names:
                tech = technologies_by_name.get(tech_name)
                if tech is not None:
                    project.technologies.add(tech)

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Created project: {project.title}")
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Updated project: {project.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Import completed! {len(projects_data)} projects processed. "
                f"Created: {created_count}, Updated: {updated_count}"
            )
        )
