from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Technology(models.Model):
    """Represents a technology, framework, or tool used in projects."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ("backend", "Backend"),
            ("frontend", "Frontend"),
            ("database", "Database"),
            ("tool", "Tool"),
            ("language", "Language"),
        ],
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon name (e.g., 'python', 'django', 'postgresql')",
    )
    color = models.CharField(
        max_length=7,
        default="#ff6b35",
        help_text="HEX color for badges",
    )
    proficiency = models.IntegerField(
        default=3,
        choices=[(i, f"{i}/5") for i in range(1, 6)],
        help_text="Mastery level out of 5",
    )
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Project category (e.g., Backend CLI, Fullstack, REST API)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#ff6b35")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    """Represents a portfolio project with a unique visual identity."""

    # Base info
    title = models.CharField(max_length=200, verbose_name="Title")
    slug = models.SlugField(unique=True, max_length=200)
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
        default="#ff6b35",
        help_text="Primary HEX color",
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#f7931e",
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
    completed_at = models.DateField(help_text="Project completion date", null=True, blank=True)
    duration = models.CharField(
        max_length=50,
        blank=True,
        help_text="Project duration (e.g., '3 months', '2 weeks')",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Publish this project",
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (0 = first)",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-completed_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def gradient_css(self) -> str:
        """Return CSS string for the project's gradient."""
        return f"linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%)"

    def get_similar_projects(self, limit: int = 3):
        """Return published projects sharing technologies with this one."""
        return (
            Project.objects.filter(technologies__in=self.technologies.all(), is_published=True)
            .exclude(id=self.id)
            .distinct()
            .order_by("-is_featured", "-completed_at")[:limit]
        )


class ProjectImage(models.Model):
    """Additional gallery images for a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project image"
        verbose_name_plural = "Project images"

    def __str__(self) -> str:
        return f"{self.project.title} - Image {self.order}"
