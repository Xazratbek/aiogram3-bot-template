from __future__ import annotations

from collections.abc import Callable

from .messages import DEFAULT_LOCALE, MESSAGES


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    code = locale.split("-")[0].lower()
    return code if code in MESSAGES else DEFAULT_LOCALE


def get_translator(locale: str | None) -> Callable[[str], str]:
    normalized = normalize_locale(locale)
    bundle = MESSAGES.get(normalized, MESSAGES[DEFAULT_LOCALE])

    def translate(key: str, **kwargs: object) -> str:
        text = bundle.get(key) or MESSAGES[DEFAULT_LOCALE].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

    return translate


def available_locales() -> tuple[str, ...]:
    return tuple(MESSAGES.keys())
