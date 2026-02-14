"""Command-line interface for the Domino's PL promotions scraper.

For programmatic usage, import the library directly instead::

    from dominospl_promo import get_promotions
"""

from config import load_config
from dominospl_promo import get_promotions
from i18n import I18n


def main() -> None:
    """Load config and print all current pizza promotions."""
    cfg = load_config()
    i18n = I18n(cfg.get("language", "pl"))
    debug: bool = cfg.get("debug", False)

    print(i18n.t("fetching"))
    promos = get_promotions(debug=debug)

    if not promos:
        print(i18n.t("no_promotions"))
        return

    print(f"\n{i18n.t('found_promotions', count=len(promos))}\n")
    for promo in promos:
        print(f"  {promo['description'][:100]}...")
        print()


if __name__ == "__main__":
    main()
