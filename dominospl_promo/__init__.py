"""dominospl_promo — Domino's Pizza Poland promotions scraper.

Quickstart::

    from dominospl_promo import get_promotions

    for promo in get_promotions():
        print(promo["description"], promo["price"])

Each promotion dict returned by :func:`get_promotions` contains:

- ``description`` (str): Promotion text (max 300 chars).
- ``price`` (float): Price in PLN as found in the promotion text.

Results are sorted by ``price`` ascending.
"""

from dominospl_promo.parser import parse_promotions
from dominospl_promo.scraper import fetch_promotions_html


def get_promotions(debug: bool = False) -> list[dict]:
    """Fetch and return current pizza promotions from dominospizza.pl.

    Args:
        debug: When True, the parser prints a detailed accept/reject log
               for every div it inspects.

    Returns:
        List of dicts with keys ``description`` (str) and ``price`` (float),
        sorted by price ascending.

    Example::

        from dominospl_promo import get_promotions

        cheapest = get_promotions()[0]
        print(cheapest["description"], "—", cheapest["price"], "PLN")
    """
    html = fetch_promotions_html()
    return parse_promotions(html, debug=debug)
