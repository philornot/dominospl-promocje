"""HTML parsing utilities for extracting promotion data from Domino's pages."""

import re

from bs4 import BeautifulSoup

_MIN_PIZZA_PRICE = 12.0
_MAX_DIV_TEXT_LEN = 500

_SAVINGS_PATTERN = re.compile(
    r"(oszczędzasz|taniej|zniżk|rabat|gratis|za\s+0)\s*[\d,.]",
    re.IGNORECASE,
)
_NON_PIZZA_KEYWORDS = re.compile(
    r"\b(napój|napoje|zapiekanka|skrzydełka|nuggets?|deser|lody|sos)\b",
    re.IGNORECASE,
)


def _extract_price(text: str) -> float | None:
    """Extract the first plausible offer price from a promotional text string.

    Args:
        text: Raw promotional text.

    Returns:
        Price as a float, or None if no valid price was found.
    """
    cleaned = _SAVINGS_PATTERN.sub("__SAVING__ ", text)
    for match in re.finditer(r"(\d+[,.]?\d*)\s*z[łl\u0142]", cleaned, re.IGNORECASE):
        value = float(match.group(1).replace(",", "."))
        if value >= _MIN_PIZZA_PRICE:
            return value
    return None


def _is_pizza_promo(text: str) -> bool:
    """Return True if text represents a pizza promotion.

    Args:
        text: Full text content of a div element.

    Returns:
        True if the div mentions pizza and is not a non-pizza-only item.
    """
    has_pizza = bool(re.search(r"pizz", text, re.IGNORECASE))
    has_only_sides = bool(_NON_PIZZA_KEYWORDS.search(text)) and not has_pizza
    return has_pizza and not has_only_sides


def parse_promotions(html: str, debug: bool = False) -> list[dict]:
    """Parse raw HTML and return a list of pizza promotion dicts.

    Each dict contains:
        - ``description`` (str): Promotion text, truncated to 300 characters.
        - ``price`` (float): Price found in the promotion text, in PLN.

    Results are sorted by ``price`` ascending. Duplicate ``(description, price)``
    pairs are removed.

    Args:
        html: Rendered HTML from the Domino's promotions page.
        debug: Print accept/reject log for every candidate div.

    Returns:
        List of promotion dicts.
    """
    soup = BeautifulSoup(html, "html.parser")
    seen: set[tuple[str, float]] = set()
    promos: list[dict] = []

    for div in soup.select("div"):
        text = div.get_text(" ", strip=True)

        if len(text) > _MAX_DIV_TEXT_LEN:
            if debug:
                print(f"[DEBUG] SKIP (too long, {len(text)} chars): {text[:80]!r}")
            continue

        price = _extract_price(text)
        if not price:
            if debug:
                print(f"[DEBUG] SKIP (no valid price): {text[:80]!r}")
            continue

        if not _is_pizza_promo(text):
            if debug:
                print(f"[DEBUG] SKIP (not pizza): {text[:80]!r}")
            continue

        description = text[:300]
        key = (description, price)
        if key in seen:
            if debug:
                print(f"[DEBUG] SKIP (duplicate): {text[:80]!r}")
            continue
        seen.add(key)

        if debug:
            print(f"[DEBUG] ACCEPT price={price}: {text[:80]!r}")

        promos.append({"description": description, "price": price})

    promos.sort(key=lambda x: x["price"])
    return promos
