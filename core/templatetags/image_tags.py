from django import template
from django.templatetags.static import static


register = template.Library()


@register.simple_tag
def project_image(project, default: str = 'img/placeholder-project.jpg') -> str:
    """Return project featured image URL or a static placeholder.

    Args:
        project: Project instance to read the featured image from.
        default: Static path for placeholder if no image.

    Returns:
        Absolute/relative URL to the image to display.
    """
    try:
        if getattr(project, 'featured_image', None) and project.featured_image.name:
            return project.featured_image.url
    except Exception:
        # If file missing or storage error, fallback to static
        pass
    return static(default)


