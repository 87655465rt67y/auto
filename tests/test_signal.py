from unittest.mock import MagicMock, patch

from auto.signal import send_workflow_signal


def test_send_workflow_signal_success() -> None:
    mock_page = MagicMock()
    mock_more_btn = MagicMock()
    mock_signal_item = MagicMock()
    mock_signal_item.count.return_value = 1
    mock_select_btn = MagicMock()
    mock_option = MagicMock()
    mock_submit_btn = MagicMock()
    mock_submit_btn.is_enabled.return_value = True

    def locator_side_effect(selector: str) -> MagicMock:
        if 'button:has-text("More Actions")' in selector:
            return mock_more_btn
        if 'li[data-testid="signal-button"]' in selector:
            return mock_signal_item
        if 'button[data-testid="signal-select-button"]' in selector:
            return mock_select_btn
        if 'li[role="option"]:has-text("retry_upload")' in selector:
            return mock_option
        if 'button[data-testid="confirm-modal-button"]' in selector:
            return mock_submit_btn
        return MagicMock()

    mock_page.locator.side_effect = locator_side_effect

    with patch("time.sleep") as mock_sleep:
        send_workflow_signal(
            mock_page, signal_name="retry_upload", post_signal_delay=5.0
        )

    mock_more_btn.click.assert_called_once()
    mock_signal_item.click.assert_called_once()
    mock_select_btn.click.assert_called_once()
    mock_option.click.assert_called_once()
    mock_submit_btn.click.assert_called_once()
    mock_sleep.assert_any_call(2.0)
    mock_sleep.assert_any_call(5.0)


def test_send_workflow_signal_fallback_item() -> None:
    mock_page = MagicMock()
    mock_more_btn = MagicMock()
    mock_signal_item_testid = MagicMock()
    mock_signal_item_testid.count.return_value = 0
    mock_signal_item_text = MagicMock()
    mock_select_btn = MagicMock()
    mock_option = MagicMock()
    mock_submit_btn = MagicMock()
    mock_submit_btn.is_enabled.return_value = True

    def locator_side_effect(selector: str) -> MagicMock:
        if 'button:has-text("More Actions")' in selector:
            return mock_more_btn
        if 'li[data-testid="signal-button"]' in selector:
            return mock_signal_item_testid
        if 'li:has-text("Send a Signal")' in selector:
            return mock_signal_item_text
        if 'button[data-testid="signal-select-button"]' in selector:
            return mock_select_btn
        if 'li[role="option"]' in selector:
            return mock_option
        if 'button[data-testid="confirm-modal-button"]' in selector:
            return mock_submit_btn
        return MagicMock()

    mock_page.locator.side_effect = locator_side_effect

    with patch("time.sleep"):
        send_workflow_signal(mock_page)

    mock_signal_item_text.click.assert_called_once()
    mock_submit_btn.click.assert_called_once()
