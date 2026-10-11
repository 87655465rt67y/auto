import re
import time

from playwright.sync_api import Page


def select_cities_and_open_modal(page: Page) -> bool:
    """Switch to Cities tab, select all errors, and open modal."""
    tab = page.locator('button[role="tab"]:has-text("Cities")')
    tab.click()
    time.sleep(2.0)
    badge = tab.locator("div").first
    badge_text = badge.inner_text().strip() if badge.count() else "0"
    digits = re.findall(r"\d+", badge_text)
    if not digits or int(digits[0]) == 0:
        return False
    cb = page.locator('button[role="checkbox"][aria-label="Select all"]')
    if cb.count() and cb.get_attribute("data-state") != "checked":
        cb.click()
        time.sleep(1.0)
    for btn in page.locator('button:has-text("Resolve all")').all():
        if btn.is_enabled():
            btn.click()
            break
    time.sleep(3.0)
    return True


def suggest_and_resolve(page: Page, post_resolve_delay: float = 10.0) -> int:
    """Trigger AI suggestion and click enabled Resolve button."""
    dialog = page.locator('div[role="dialog"]')
    dialog.locator('button:has-text("Suggest with AI")').click()
    time.sleep(5.0)
    btn = dialog.locator('button:has-text("Resolve ")')
    for _ in range(5):
        if btn.is_enabled():
            break
        time.sleep(1.0)
    match = re.search(r"\d+", btn.inner_text())
    count = int(match.group()) if match else 0
    if btn.is_enabled() and count > 0:
        btn.click()
        time.sleep(post_resolve_delay)
    return count
