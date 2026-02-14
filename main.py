import re

import yaml
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DOMINOS = "https://www.dominospizza.pl"


def load_config():
    """Load configuration from config.yaml file.

    Returns:
        dict: Configuration dictionary with address and user settings.
    """
    with open("config.yaml", encoding="utf8") as f:
        return yaml.safe_load(f)


def extract_price(text):
    """Extract price from text containing Polish currency format.

    Args:
        text (str): Text containing price information.

    Returns:
        float: Extracted price or None if not found.
    """
    m = re.search(r'(\d+[,.]?\d*)\s*zł', text.lower())
    if m:
        return float(m.group(1).replace(",", "."))
    return None


def extract_pizzas(text):
    """Extract number of pizzas from promotional text.

    Args:
        text (str): Promotional text containing pizza count.

    Returns:
        int: Number of pizzas, defaults to 1 if not found.
    """
    m = re.search(r'(\d+)\s*pizz', text.lower())
    return int(m.group(1)) if m else 1


def decline_pizza(count):
    """Decline the word 'pizza' according to Polish grammar rules.

    Args:
        count (int): Number of pizzas.

    Returns:
        str: Properly declined word (pizza/pizze/pizz).
    """
    if count == 1:
        return "pizza"
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return "pizze"
    else:
        return "pizz"


def get_promotions(cfg):
    """Scrape Domino's Pizza promotions for given address.

    Args:
        cfg (dict): Configuration containing address details.

    Returns:
        list: List of promotion dictionaries with price and pizza info.
    """
    city = cfg["address"]["city"]
    street = cfg["address"]["street"]
    house = cfg["address"]["house_number"]

    promos = []

    with sync_playwright() as p:
        # Launch browser with anti-detection settings
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )

        # Create context with realistic browser fingerprint
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='pl-PL',
            timezone_id='Europe/Warsaw'
        )

        page = context.new_page()

        # ================= OPEN =================

        print("Opening Domino's website...")
        page.goto(DOMINOS, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)  # Wait for dynamic content

        # ================= COOKIES =================

        print("Handling cookies popup...")
        try:
            page.wait_for_selector("#onetrust-reject-all-handler", timeout=5000)
            page.click("#onetrust-reject-all-handler")
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"No cookie popup or already handled: {e}")

        # ================= ADDRESS POPUP =================

        print(f"Setting address: {city}, {street} {house}")

        try:
            # Wait for address popup to appear
            page.wait_for_selector("#City", timeout=10000, state="visible")

            # Fill city
            page.fill("#City", city)
            page.wait_for_timeout(500)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

            # Fill street
            page.fill("#Street", street)
            page.wait_for_timeout(500)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)

            # Fill house number
            page.fill("#HouseNr", house)
            page.wait_for_timeout(500)

            # Click DALEJ (delivery section)
            print("Submitting address...")
            page.click('div[data-popupchangeplace-section="1"] button[type="submit"]')

            # Wait until popup disappears (address accepted)
            page.wait_for_selector(".m-PopupChangePlace", state="detached", timeout=15000)
            print("Address confirmed!")
            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"Error during address setup: {e}")
            print("Trying to continue anyway...")

        # ================= PROMOTIONS =================

        print("Navigating to promotions page...")
        page.goto(f"{DOMINOS}/menu/promocje", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)  # Wait for promotions to load

        # Scroll down to load lazy-loaded content
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(500)

        soup = BeautifulSoup(page.content(), "html.parser")

        print("Parsing promotions...")

        # Look for promotion cards - adjust selectors based on actual page structure
        for div in soup.select("div"):
            text = div.get_text(" ", strip=True)

            price = extract_price(text)
            if not price:
                continue

            pizzas = extract_pizzas(text)

            promos.append({
                "description": text,
                "price": price,
                "pizzas": pizzas,
                "price_per_pizza": round(price / pizzas, 2)
            })

        browser.close()

    return promos


if __name__ == "__main__":

    cfg = load_config()
    wanted = cfg["user"]["pizzas_wanted"]

    print(f"\n🍕 Looking for best deals for {wanted} pizzas...\n")

    promos = get_promotions(cfg)

    # Remove duplicates based on description similarity
    unique_promos = []
    seen_prices = set()
    for p in promos:
        key = (p['price'], p['pizzas'])
        if key not in seen_prices:
            seen_prices.add(key)
            unique_promos.append(p)

    unique_promos.sort(key=lambda x: x["price_per_pizza"])

    print(f"\n🔥 Best promotions (found {len(unique_promos)}):\n")

    for p in unique_promos[:5]:
        print(f"📦 {p['description'][:100]}...")
        print(f"   💰 {p['price']} zł / {p['pizzas']} {decline_pizza(p['pizzas'])}")
        print(f"   ⭐ {p['price_per_pizza']} zł per pizza\n")
