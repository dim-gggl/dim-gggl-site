from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.utils import optimize_image


# Custom validators
def validate_hex_color(value):
    """Validate that a string is a valid HEX color code."""
    if not value.startswith("#") or len(value) != 7:
        raise ValidationError(
            f"{value} is not a valid HEX color code (must be #RRGGBB)"
        )
    try:
        int(value[1:], 16)
    except ValueError:
        raise ValidationError(f"{value} is not a valid HEX color code")


# Custom managers
class PublishedManager(models.Manager):
    """Manager that returns only published items."""

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Technology(models.Model):
    """Represents a technology, framework, or tool used in projects."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ("backend", "Backend"),
            ("frontend", "Frontend"),
            ("database", "Database"),
            ("tool", "Tool"),
            ("language", "Language"),
        ],
        db_index=True,
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name (e.g., 'python', 'django', 'postgresql')",
    )
    color = models.CharField(
        max_length=7,
        default="#ff6b35",
        validators=[validate_hex_color],
        help_text="HEX color for badges",
    )
    proficiency = models.IntegerField(
        default=3,
        choices=[(i, f"{i}/5") for i in range(1, 6)],
        help_text="Mastery level out of 5",
    )
    order = models.IntegerField(default=0, help_text="Display order", db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        indexes = [
            models.Index(fields=["category", "proficiency"]),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Project category (e.g., Backend CLI, Fullstack, REST API)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(
        max_length=7,
        default="#ff6b35",
        validators=[validate_hex_color],
    )
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Represents a portfolio project with a unique visual identity."""

    # Base info
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, max_length=200, db_index=True)
    tagline = models.CharField(
        max_length=200,
        help_text="Short one-line tagline",
        blank=True,
        default="",
    )
    description = models.TextField(
        help_text="Detailed project description (markdown supported)",
        blank=True,
        default="",
    )

    # Visual identity
    primary_color = models.CharField(
        max_length=7,
        default="#95ff17",
        validators=[validate_hex_color],
        help_text="Primary HEX color",
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#f7931e",
        validators=[validate_hex_color],
        help_text="Secondary HEX color",
    )
    background_style = models.CharField(
        max_length=20,
        choices=[
            ("solid", "Solid color"),
            ("gradient", "Gradient"),
            ("pattern", "Pattern"),
            ("image", "Image"),
        ],
        default="gradient",
    )

    # Media
    featured_image = models.ImageField(
        upload_to="projects/featured/",
        blank=True,
        help_text="Primary image (recommended 1200x630px)",
    )
    logo = models.ImageField(
        upload_to="projects/logos/",
        blank=True,
        help_text="Optional project logo",
    )

    # Categorization and relations
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="projects",
        db_index=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        help_text="Technologies used in this project",
    )

    # Technical details
    challenges = models.TextField(
        blank=True,
        help_text="Challenges and how they were solved",
    )
    learnings = models.TextField(
        blank=True,
        help_text="Key learnings from this project",
    )
    features = models.JSONField(
        default=list,
        help_text="List of main features (JSON array)",
    )

    # External links
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    demo_url = models.URLField(blank=True, verbose_name="Demo URL")
    documentation_url = models.URLField(blank=True, verbose_name="Documentation URL")

    # Metadata
    completed_at = models.DateField(
        help_text="Project completion date",
        null=True,
        blank=True,
        db_index=True,
    )
    duration = models.CharField(
        max_length=50,
        blank=True,
        help_text="Project duration (e.g., '3 months', '2 weeks')",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage",
        db_index=True,
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Publish this project",
        db_index=True,
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (0 = first)",
        db_index=True,
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["order", "-completed_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        indexes = [
            models.Index(fields=["is_published", "is_featured", "order"]),
            models.Index(fields=["is_published", "order", "-completed_at"]),
            models.Index(fields=["category", "is_published"]),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        """
        Auto-generate slug and optimize featured image.
        Note: Image optimization is synchronous - consider using Celery for async processing.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        # Only optimize if it's a new image (not already committed)
        if self.featured_image and not getattr(
            self.featured_image, "_committed", False
        ):
            try:
                self.featured_image = optimize_image(self.featured_image)
            except Exception as e:
                # Log the error but don't block the save
                import logging

                logger = logging.getLogger("portfolio")
                logger.error(f"Failed to optimize image for project {self.title}: {e}")

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Return the canonical URL for this project."""
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def gradient_css(self) -> str:
        """Return CSS string for the project's gradient background."""
        return f"linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%)"

    def get_similar_projects(self, limit: int = 3):
        """
        Return published projects similar to this one.
        Prioritizes projects with same category and shared technologies.

        Args:
            limit: Maximum number of similar projects to return

        Returns:
            QuerySet of Project objects
        """
        from django.db.models import Count, Q

        similar = (
            Project.published.exclude(id=self.id)
            .filter(
                Q(category=self.category) | Q(technologies__in=self.technologies.all())
            )
            .annotate(
                same_category=Count("id", filter=Q(category=self.category)),
                shared_techs=Count(
                    "technologies", filter=Q(technologies__in=self.technologies.all())
                ),
            )
            .order_by("-same_category", "-shared_techs", "order", "-completed_at")
            .distinct()[:limit]
        )

        return similar


class ProjectImage(models.Model):
    """Additional gallery images for a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project image"
        verbose_name_plural = "Project images"

    def __str__(self) -> str:
        return f"{self.project.title} - Image {self.order}"

    def save(self, *args, **kwargs):
        """Optimize gallery images on save."""
        if self.image and not getattr(self.image, "_committed", False):
            try:
                self.image = optimize_image(self.image)
            except Exception as e:
                import logging

                logger = logging.getLogger("portfolio")
                logger.error(
                    f"Failed to optimize gallery image for project {self.project.title}: {e}"
                )
        super().save(*args, **kwargs)
