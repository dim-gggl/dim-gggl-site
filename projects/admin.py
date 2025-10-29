from django.contrib import admin
from django.utils.html import format_html
from .models import Technology, Category, Project, ProjectImage


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency_display", "color_badge", "order"]
    list_filter = ["category", "proficiency"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]

    def color_badge(self, obj):
        return format_html(
            '<span style="background:{}; color:white; padding:4px 8px; border-radius:4px;">{}</span>',
            obj.color,
            obj.name,
        )

    color_badge.short_description = "Badge"

    def proficiency_display(self, obj):
        stars = "⭐" * obj.proficiency
        return format_html('<span title="{}/5">{}</span>', obj.proficiency, stars)

    proficiency_display.short_description = "Proficiency"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "projects_count", "color_badge", "order"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["order"]

    def color_badge(self, obj):
        return format_html(
            '<span style="background:{}; color:white; padding:4px 8px; border-radius:4px;">{}</span>',
            obj.color,
            obj.name,
        )

    color_badge.short_description = "Badge"

    def projects_count(self, obj):
        return obj.projects.count()

    projects_count.short_description = "Projects"


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
    list_filter = ["is_featured", "is_published", "category", "technologies"]
    search_fields = ["title", "description", "tagline"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_featured", "is_published", "order"]
    date_hierarchy = "completed_at"
    filter_horizontal = ["technologies"]
    inlines = [ProjectImageInline]

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

    def color_preview(self, obj):
        return format_html(
            '<div style="width:60px; height:20px; background:{}; border-radius:4px;"></div>',
            obj.gradient_css,
        )

    color_preview.short_description = "Colors"

    def tech_count(self, obj):
        return obj.technologies.count()

    tech_count.short_description = "Technologies"
