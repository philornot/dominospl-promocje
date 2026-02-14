"""Internationalization for the dominospl_promo CLI.

Supported languages: Polish (pl), English (en).
"""

TRANSLATIONS: dict[str, dict[str, str]] = {
    "pl": {
        "fetching": "Pobieram promocje z dominospizza.pl...",
        "found_promotions": "Znalezione promocje ({count}):",
        "no_promotions": "Nie znaleziono żadnych promocji z pizzą.",
    },
    "en": {
        "fetching": "Fetching promotions from dominospizza.pl...",
        "found_promotions": "Promotions found ({count}):",
        "no_promotions": "No pizza promotions found.",
    },
}

SUPPORTED_LANGUAGES = list(TRANSLATIONS.keys())


class I18n:
    """Locale-aware message formatter.

    Args:
        language: Language code ('pl' or 'en').

    Raises:
        ValueError: If *language* is not supported.
    """

    def __init__(self, language: str) -> None:
        if language not in TRANSLATIONS:
            raise ValueError(f"Unsupported language '{language}'. Choose one of: {SUPPORTED_LANGUAGES}")
        self._strings = TRANSLATIONS[language]

    def t(self, key: str, **kwargs) -> str:
        """Translate and format a message.

        Args:
            key: Translation key.
            **kwargs: Interpolation values.

        Returns:
            Formatted string.
        """
        return self._strings[key].format(**kwargs)
