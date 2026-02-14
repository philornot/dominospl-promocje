"""Playwright-based HTML fetcher for the Domino's Poland promotions page."""

from playwright.sync_api import sync_playwright

_PROMOTIONS_URL = "https://www.dominospizza.pl/menu/promocje"

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def fetch_promotions_html() -> str:
    """Fetch the raw HTML of the Domino's Poland promotions page.

    Uses a headless Chromium browser to execute JavaScript and load
    lazy content before returning the fully-rendered HTML.

    Returns:
        Raw HTML string of the rendered promotions page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=_USER_AGENT,
            locale="pl-PL",
            timezone_id="Europe/Warsaw",
        )
        page = context.new_page()
        page.goto(_PROMOTIONS_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        for _ in range(3):
            page.evaluate("window.scrollBy(0, 500)")
            page.wait_for_timeout(500)

        html = page.content()
        browser.close()

    return html
