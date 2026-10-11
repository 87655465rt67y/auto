import time

from playwright.sync_api import Page


def send_workflow_signal(
    page: Page,
    signal_name: str = "retry_upload",
    post_signal_delay: float = 5.0,
) -> None:
    page.locator('button:has-text("More Actions")').click()
    signal_item = page.locator('li[data-testid="signal-button"]')
    if not signal_item.count():
        signal_item = page.locator('li:has-text("Send a Signal")')
    signal_item.click()
    time.sleep(2.0)

    page.locator('button[data-testid="signal-select-button"]').click()
    page.locator(f'li[role="option"]:has-text("{signal_name}")').click()

    submit_btn = page.locator('button[data-testid="confirm-modal-button"]')
    for _ in range(5):
        if submit_btn.is_enabled():
            break
        time.sleep(0.5)
    submit_btn.click()
    time.sleep(post_signal_delay)
