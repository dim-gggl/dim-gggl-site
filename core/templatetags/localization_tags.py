"""
Template tags and filters for application-managed translations.
"""

from __future__ import annotations

from django import template

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
