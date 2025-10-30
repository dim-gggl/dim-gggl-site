from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def lazy_img(src, alt="", css_class="", width=None, height=None, fallback=None, **extra_attrs):
    """Return an <img> tag configured for lazy loading."""

    placeholder = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'"
        f" viewBox='0 0 {width or 800} {height or 600}'%3E%3C/svg%3E"
    )
    classes = "lazy"
    if css_class:
        classes = f"{classes} {css_class}"

    attributes = [
        f'src="{placeholder}"',
        f'data-src="{src}"',
        f'alt="{alt}"',
        f'class="{classes}"',
        'loading="lazy"',
    ]

    if width:
        attributes.append(f'width="{width}"')
    if height:
        attributes.append(f'height="{height}"')

    if fallback and "onerror" not in extra_attrs:
        extra_attrs["onerror"] = (
            "this.onerror=null; this.src='{url}'; this.classList.remove('lazy');"
        ).format(url=fallback)

    for key, value in extra_attrs.items():
        html_key = key.replace("_", "-")
        attributes.append(f'{html_key}="{value}"')

    tag = f"<img {' '.join(attributes)}>"
    return mark_safe(tag)

