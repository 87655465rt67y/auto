import time

from playwright.sync_api import BrowserContext, Page, Playwright, sync_playwright

from auto.auth import is_login_page, login
from auto.browser import launch_browser_context
from auto.cities import select_cities_and_open_modal, suggest_and_resolve
from auto.config import Settings, get_settings
from auto.models import BrandItem


class FirstwatchSession:
    """Manages persistent browser session for Firstwatch."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    @property
    def page(self) -> Page:
        if self._page is None:
            raise RuntimeError("Session not started. Call start() first.")
        return self._page

    def start(self) -> Page:
        self._playwright = sync_playwright().start()
        self._context = launch_browser_context(self._playwright, self.settings)
        pages = self._context.pages
        self._page = pages[0] if pages else self._context.new_page()
        self.navigate(self.settings.base_url)
        return self._page

    def navigate(self, url: str) -> None:
        if self._page is None:
            raise RuntimeError("Session not started. Call start() first.")
        self._page.goto(url, wait_until="domcontentloaded")
        time.sleep(self.settings.nav_delay)
        if is_login_page(self._page):
            login(self._page, self.settings)
            self._page.goto(url, wait_until="domcontentloaded")
            time.sleep(self.settings.nav_delay)

    def resolve_city_errors(self) -> tuple[list[BrandItem], int]:
        ok, brands = select_cities_and_open_modal(self.page)
        if not ok:
            return [], 0
        return brands, suggest_and_resolve(
            self.page, self.settings.post_resolve_delay
        )

    def close(self) -> None:
        if self._context is not None:
            self._context.close()
        if self._playwright is not None:
            self._playwright.stop()
