import time

from playwright.sync_api import Error, Page, TimeoutError

from auto.config import Settings
from auto.models import BrandItem
from auto.signal import send_workflow_signal


def handle_sso_if_needed(page: Page, timeout: float = 60.0) -> None:
    btn = page.locator('button[data-testid="login-button"]')
    if not btn.count():
        btn = page.locator('button:has-text("Continue to SSO")')
    if btn.count() and btn.first.is_visible():
        btn.first.click()
        try:
            page.wait_for_selector(
                "#per-page-filter", timeout=int(timeout * 1000)
            )
        except (TimeoutError, Error):
            time.sleep(timeout)


def select_per_page_500(page: Page, delay: float = 5.0) -> None:
    page.select_option("#per-page-filter", "500")
    time.sleep(delay)


def find_and_click_workflow(
    page: Page, brands: list[BrandItem]
) -> str | None:
    for item in brands:
        for row in page.locator("tbody.holocene-table-body tr").all():
            link = row.locator("a.link").first
            if link.count() and item.brand in link.inner_text():
                text = link.inner_text().strip()
                link.click()
                return text
    return None


def run_orchestrator(
    page: Page, brands: list[BrandItem], settings: Settings
) -> str | None:
    page.goto(settings.orchestrator_url, wait_until="domcontentloaded")
    time.sleep(settings.orchestrator_delay)
    handle_sso_if_needed(page, settings.sso_timeout)
    select_per_page_500(page, settings.orchestrator_delay)
    matched = find_and_click_workflow(page, brands)
    if matched:
        time.sleep(settings.orchestrator_delay)
        send_workflow_signal(
            page, post_signal_delay=settings.orchestrator_delay
        )
    return matched
