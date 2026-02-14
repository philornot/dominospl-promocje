"""dominospl_promo — Domino's Pizza Poland promotions scraper.

Quickstart::

    from dominospl_promo import get_promotions

    for promo in get_promotions():
        print(promo["description"], promo["price_per_pizza"])

Each promotion dict returned by :func:`get_promotions` contains:

- ``description`` (str): Promotion text (max 300 chars).
- ``price`` (float): Total price in PLN.
- ``pizzas`` (int): Number of pizzas included in the deal.
- ``price_per_pizza`` (float): ``price / pizzas``, rounded to 2 decimal places.

Results are sorted by ``price_per_pizza`` ascending.
"""

from dominospl_promo.parser import parse_promotions
from dominospl_promo.scraper import fetch_promotions_html


def get_promotions(debug: bool = False) -> list[dict]:
    """Fetch and return current pizza promotions from dominospizza.pl.

    Launches a headless browser, loads the promotions page, and parses
    all pizza deals found. Takes ~5–8 seconds due to page rendering.

    Args:
        debug: When True, the parser prints a detailed accept/reject log
               for every div it inspects. Useful for diagnosing missing
               promotions after a site redesign.

    Returns:
        List of promotion dicts sorted by price_per_pizza ascending.
        See module docstring for dict structure.

    Example::

        from dominospl_promo import get_promotions

        promos = get_promotions()
        cheapest = promos[0]
        print(f"{cheapest['description']} — {cheapest['price_per_pizza']} PLN/pizza")
    """
    html = fetch_promotions_html()
    return parse_promotions(html, debug=debug)
