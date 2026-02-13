import re

import yaml
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DOMINOS = "https://www.dominospizza.pl"


def load_config():
    with open("config.yaml", encoding="utf8") as f:
        return yaml.safe_load(f)


def extract_price(text):
    m = re.search(r'(\d+[,.]?\d*)\s*zł', text.lower())
    if m:
        return float(m.group(1).replace(",", "."))
    return None


def extract_pizzas(text):
    m = re.search(r'(\d+)\s*pizz', text.lower())
    return int(m.group(1)) if m else 1


def get_promotions(cfg):
    city = cfg["address"]["city"]
    street = cfg["address"]["street"]
    house = cfg["address"]["house_number"]

    promos = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False) # dla debugu false
        page = browser.new_page()

        # ================= OPEN =================

        page.goto(DOMINOS, wait_until="networkidle")

        # ================= COOKIES =================

        try:
            page.wait_for_selector("#onetrust-reject-all-handler", timeout=5000)
            page.click("#onetrust-reject-all-handler")
        except:
            pass

        # ================= ADDRESS POPUP =================

        page.wait_for_selector("#City")

        page.fill("#City", city)
        page.keyboard.press("Enter")

        page.fill("#Street", street)
        page.keyboard.press("Enter")

        page.fill("#HouseNr", house)

        # click DALEJ (delivery section)

        page.click('div[data-popupchangeplace-section="1"] button[type="submit"]')

        # wait until popup disappears (address accepted)

        page.wait_for_selector(".m-PopupChangePlace", state="detached", timeout=15000)

        # ================= PROMOTIONS =================

        page.goto(f"{DOMINOS}/deals", wait_until="networkidle")

        soup = BeautifulSoup(page.content(), "html.parser")

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

    promos = get_promotions(cfg)

    promos.sort(key=lambda x: x["price_per_pizza"])

    print("\n🔥 Najlepsze promocje:\n")

    for p in promos[:5]:
        print(p["description"])
        print(f"{p['price']} zł / {p['pizzas']} pizz")
        print(f"=> {p['price_per_pizza']} zł za pizzę\n")
