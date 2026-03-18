"""
Application translation service.

This module centralizes language normalization and catalog lookups so the UI
and dynamic project content can share the same runtime behavior.
"""

from __future__ import annotations

from django.utils.translation import get_language

from core.localization.content_catalog import CONTENT_TRANSLATIONS, UI_TRANSLATIONS

DEFAULT_LANGUAGE = "en"


def normalize_language_code(language_code: str | None) -> str:
    """
    Normalize a Django language code to the short form used by the catalog.

    Args:
        language_code: Django language code such as ``fr`` or ``fr-fr``.

    Returns:
        str: Normalized language code supported by the catalog.
    """

    if not language_code:
        return DEFAULT_LANGUAGE
    short_code = language_code.split("-")[0].lower()
    return short_code if short_code in UI_TRANSLATIONS else DEFAULT_LANGUAGE


def get_current_language() -> str:
    """
    Return the active normalized language code.

    Returns:
        str: Current language code supported by the catalog.
    """

    return normalize_language_code(get_language())


def translate_key(key: str, language_code: str | None = None, **kwargs) -> str:
    """
    Translate a UI key using the application catalog.

    Args:
        key: Catalog key.
        language_code: Optional target language code.
        **kwargs: Optional format values interpolated into the string.

    Returns:
        str: Localized string if found, otherwise the key itself.
    """

    language = normalize_language_code(language_code or get_current_language())
    message = UI_TRANSLATIONS.get(language, {}).get(key)
    if message is None:
        message = UI_TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    return message.format(**kwargs) if kwargs else message


def translate_text(text: str | None, language_code: str | None = None) -> str | None:
    """
    Translate free-form content using exact English source strings.

    Args:
        text: Source English content.
        language_code: Optional target language code.

    Returns:
        str | None: Localized content when available, else the original text.
    """

    if text in (None, ""):
        return text

    language = normalize_language_code(language_code or get_current_language())
    if language == DEFAULT_LANGUAGE:
        return text

    return CONTENT_TRANSLATIONS.get(language, {}).get(text, text)

