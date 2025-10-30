from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Technology, Category, Project, ProjectImage


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency_display", "color_badge", "projects_count", "order"]
    list_filter = ["category", "proficiency"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]

    def get_queryset(self, request):
        """Optimize queryset with annotation."""
        queryset = super().get_queryset(request)
        return queryset.annotate(_projects_count=Count('projects'))

    @admin.display(description="Projects")
    def projects_count(self, obj):
        return obj._projects_count

    @admin.display(description="Badge")
    def color_badge(self, obj):
        return format_html(
            '<span style="background:{}; color:white; padding:4px 8px; border-radius:4px;">{}</span>',
            obj.color,
            obj.name,
        )

    @admin.display(description="Proficiency")
    def proficiency_display(self, obj):
        stars = "⭐" * obj.proficiency
        return format_html('<span title="{}/5">{}</span>', obj.proficiency, stars)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "projects_count", "color_badge", "order"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]

    def get_queryset(self, request):
        """Optimize queryset with annotation."""
        queryset = super().get_queryset(request)
        return queryset.annotate(_projects_count=Count('projects'))

    @admin.display(description="Badge")
    def color_badge(self, obj):
        return format_html(
            '<span style="background:{}; color:white; padding:4px 8px; border-radius:4px;">{}</span>',
            obj.color,
            obj.name,
        )

    @admin.display(description="Projects")
    def projects_count(self, obj):
        return obj._projects_count


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ["image", "caption", "order"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "order",
        "category",
        "completed_at",
        "is_featured",
        "is_published",
        "tech_count",
        "color_preview",
    ]
    list_filter = ["is_featured", "is_published", "category", "technologies", "created_at"]
    search_fields = ["title", "description", "tagline"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_featured", "is_published", "order"]
    date_hierarchy = "completed_at"
    filter_horizontal = ["technologies"]
    inlines = [ProjectImageInline]
    
    actions = ['mark_as_featured', 'mark_as_not_featured', 'publish', 'unpublish']

    fieldsets = (
        (
            "Main information",
            {
                "fields": ("title", "slug", "tagline", "description", "category"),
            },
        ),
        (
            "Visual identity",
            {
                "fields": (
                    "primary_color",
                    "secondary_color",
                    "background_style",
                    "featured_image",
                    "logo",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Technologies", {"fields": ("technologies",)}),
        (
            "Technical details",
            {
                "fields": ("challenges", "learnings", "features"),
                "classes": ("collapse",),
            },
        ),
        (
            "External links",
            {
                "fields": ("github_url", "demo_url", "documentation_url"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "completed_at",
                    "duration",
                    "is_featured",
                    "is_published",
                    "order",
                )
            },
        ),
    )

    @admin.display(description="Colors")
    def color_preview(self, obj):
        return format_html(
            '<div style="width:60px; height:20px; background:{}; border-radius:4px;"></div>',
            obj.gradient_css,
        )

    @admin.display(description="Technologies")
    def tech_count(self, obj):
        return obj.technologies.count()

    @admin.action(description='Mark as featured')
    def mark_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} project(s) marked as featured.')

    @admin.action(description='Remove from featured')
    def mark_as_not_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} project(s) removed from featured.')

    @admin.action(description='Publish projects')
    def publish(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'{count} project(s) published.')

    @admin.action(description='Unpublish projects')
    def unpublish(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f'{count} project(s) unpublished.')