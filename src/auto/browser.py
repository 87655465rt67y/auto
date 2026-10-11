from playwright.sync_api import BrowserContext, Playwright
from playwright_stealth import Stealth

from auto.config import Settings


def launch_browser_context(
    playwright: Playwright, settings: Settings
) -> BrowserContext:
    """Launch a persistent Playwright Chromium browser context."""
    settings.profile_dir.mkdir(parents=True, exist_ok=True)
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(settings.profile_dir),
        headless=settings.headless,
    )
    Stealth().apply_stealth_sync(context)
    return context
