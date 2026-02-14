# dominospl_promo — Domino's Pizza promotion scraper
[![PyPI](https://img.shields.io/pypi/v/dominospl-promo)](https://pypi.org/project/dominospl-promo/)
[![License](https://img.shields.io/pypi/l/dominospl-promo)](LICENSE)

Python library and CLI tool for fetching current pizza deals
from [dominospizza.pl](https://www.dominospizza.pl/menu/promocje).

> 🇵🇱 [Wersja polska (README.md)](https://github.com/philornot/dominospl-promocje/blob/master/README.md)

## Requirements

```bash
pip install playwright pyyaml beautifulsoup4
playwright install chromium
```

## Library usage

```python
from dominospl_promo import get_promotions

promos = get_promotions()

for promo in promos:
    print(promo["description"])
    print(promo["price"], "PLN /", promo["pizzas"], "pcs →", promo["price_per_pizza"], "PLN/pizza")
```

### Returned dict structure

| Key               | Type    | Description                    |
|-------------------|---------|--------------------------------|
| `description`     | `str`   | Promotion text (max 300 chars) |
| `price`           | `float` | Total price in PLN             |
| `pizzas`          | `int`   | Number of pizzas in the deal   |
| `price_per_pizza` | `float` | Price per single pizza         |

Results sorted by `price_per_pizza` ascending.

## CLI usage

### Options (`config.yaml`)

| Field      | Description                         |
|------------|-------------------------------------|
| `language` | UI language: `pl` or `en`           |
| `debug`    | Parser debug mode: `true` / `false` |

## Project structure

```
dominospl_promo/
    __init__.py     # Public API: get_promotions()
    scraper.py      # Page fetching (Playwright)
    parser.py       # HTML parsing
cli.py              # Command-line interface
i18n.py             # Translations (CLI only)
config.py           # Config loader (CLI only)
config.yaml
```