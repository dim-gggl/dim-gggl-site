"""
Template tags and filters for application-managed translations.
"""

from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from core.localization.translation_service import (
    get_current_language,
    translate_key,
    translate_text,
)


register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, key: str, **kwargs) -> str:
    """
    Translate a catalog key in templates.

    Args:
        context: Django template context.
        key: Translation key.
        **kwargs: Interpolation variables for the translation string.

    Returns:
        str: Localized UI string.
    """

    request = context.get("request")
    language_code = (
        getattr(request, "LANGUAGE_CODE", None) if request is not None else None
    )
    return translate_key(key, language_code=language_code, **kwargs)


@register.filter
def translate_content(value):
    """
    Translate dynamic content strings rendered from models.

    Args:
        value: Source text.

    Returns:
        str | None: Localized text.
    """

    return translate_text(value)


@register.simple_tag
def current_language() -> str:
    """
    Expose the active language code to templates.

    Returns:
        str: Current normalized language code.
    """

    return get_current_language()


@register.simple_tag(takes_context=True)
def intro_lines(context) -> str:
    """
    Return localized intro lines serialized as a JavaScript array literal.

    Args:
        context: Django template context.

    Returns:
        str: Safe JavaScript array literal.
    """

    request = context.get("request")
    language_code = (
        getattr(request, "LANGUAGE_CODE", None) if request is not None else None
    )
    lines = [
        translate_key(f"intro.line_{index}", language_code=language_code)
        for index in range(1, 10)
    ]
    escaped_lines = [
        line.replace("\\", "\\\\").replace('"', '\\"') for line in lines
    ]
    array_literal = "[" + ", ".join(f'"{line}"' for line in escaped_lines) + "]"
    return mark_safe(array_literal)
