import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from auto.config import Settings


def is_login_page(page: Page) -> bool:
    """Check if the current page is the sign-in page."""
    if "/login" in page.url:
        return True
    try:
        return page.locator("#email").is_visible(timeout=1000)
    except PlaywrightError:
        return False


def login(page: Page, settings: Settings) -> bool:
    """Submit credentials and wait for navigation."""
    if not is_login_page(page):
        return True
    page.fill("#email", settings.email)
    page.fill("#password", settings.password)
    page.click('button[type="submit"]')
    time.sleep(settings.nav_delay)
    return not is_login_page(page)
