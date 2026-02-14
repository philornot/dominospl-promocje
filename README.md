# dominospl_promo — skaner promocji Domino's Pizza
[![PyPI](https://img.shields.io/pypi/v/dominospl-promo)](https://pypi.org/project/dominospl-promo/)
[![License](https://img.shields.io/pypi/l/dominospl-promo)](LICENSE)


Biblioteka Pythona i narzędzie CLI do pobierania aktualnych promocji
z [dominospizza.pl](https://www.dominospizza.pl/menu/promocje).

> [English version (README-EN.md)](https://github.com/philornot/dominospl-promocje/blob/master/README-EN.md)

## Wymagania

```bash
pip install playwright pyyaml beautifulsoup4
playwright install chromium
```

## Użycie jako biblioteka

```python
from dominospl_promo import get_promotions

promos = get_promotions()

for promo in promos:
    print(promo["description"])
    print(promo["price"], "zł /", promo["pizzas"], "szt. →", promo["price_per_pizza"], "zł/pizza")
```

### Struktura zwracanego słownika

| Klucz             | Typ     | Opis                              |
|-------------------|---------|-----------------------------------|
| `description`     | `str`   | Tekst promocji (maks. 300 znaków) |
| `price`           | `float` | Łączna cena w PLN                 |
| `pizzas`          | `int`   | Liczba pizz w ofercie             |
| `price_per_pizza` | `float` | Cena za jedną pizzę               |

Wyniki posortowane rosnąco po `price_per_pizza`.

## Użycie jako CLI

### Opcje (`config.yaml`)

| Pole       | Opis                                       |
|------------|--------------------------------------------|
| `language` | Język komunikatów: `pl` lub `en`           |
| `debug`    | Tryb debugowania parsera: `true` / `false` |

## Struktura projektu

```
dominospl_promo/
    __init__.py     # Publiczne API: get_promotions()
    scraper.py      # Pobieranie strony (Playwright)
    parser.py       # Parsowanie HTML
cli.py              # Interfejs wiersza poleceń
i18n.py             # Tłumaczenia (tylko CLI)
config.py           # Ładowanie konfiguracji (tylko CLI)
config.yaml
```
