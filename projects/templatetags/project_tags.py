import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.inclusion_tag(
    "projects/components/project_meta_tags.html", takes_context=True
)
def project_meta_tags(context, project):
    """Render OpenGraph/Twitter meta tags for a project.

    Args:
        context: Template context to access request
        project: Project instance
    """
    request = context.get("request")
    absolute_url = (
        request.build_absolute_uri(project.get_absolute_url()) if request else ""
    )
    return {"project": project, "absolute_url": absolute_url, "request": request}


@register.filter(name="render_project_text")
def render_project_text(value):
    """Render project text while transforming backtick code snippets into HTML code blocks.

    Args:
        value: Raw project text that may contain Markdown-style backticks.

    Returns:
        Safe HTML string with inline (`code`) and fenced (```code```) snippets wrapped in <code>/<pre>.
    """
    if not value:
        return ""

    escaped = conditional_escape(value)

    def replace_fenced(match):
        code_content = match.group(1).strip()
        return f"<pre><code>{code_content}</code></pre>"

    def replace_inline(match):
        code_content = match.group(1)
        return f"<code>{code_content}</code>"

    fenced_pattern = re.compile(r"```(.*?)```", re.DOTALL)
    inline_pattern = re.compile(r"`([^`]+)`")

    html = fenced_pattern.sub(replace_fenced, escaped)
    html = inline_pattern.sub(replace_inline, html)
    return mark_safe(html)
