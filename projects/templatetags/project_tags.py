from django import template


register = template.Library()


@register.inclusion_tag("projects/components/project_meta_tags.html", takes_context=True)
def project_meta_tags(context, project):
    """Render OpenGraph/Twitter meta tags for a project.

    Args:
        context: Template context to access request
        project: Project instance
    """
    request = context.get("request")
    absolute_url = request.build_absolute_uri(project.get_absolute_url()) if request else ""
    return {"project": project, "absolute_url": absolute_url, "request": request}


