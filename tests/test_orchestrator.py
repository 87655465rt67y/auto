from unittest.mock import MagicMock, patch

from auto.config import Settings
from auto.models import BrandItem
from auto.orchestrator import (
    find_and_click_workflow,
    handle_sso_if_needed,
    run_orchestrator,
    select_per_page_500,
)


def test_handle_sso_when_button_visible() -> None:
    mock_page = MagicMock()
    mock_btn = MagicMock()
    mock_btn.count.return_value = 1
    mock_btn.first.is_visible.return_value = True
    mock_page.locator.return_value = mock_btn

    handle_sso_if_needed(mock_page, timeout=5.0)

    mock_btn.first.click.assert_called_once()
    mock_page.wait_for_selector.assert_called_once_with(
        "#per-page-filter", timeout=5000
    )


def test_handle_sso_when_button_absent() -> None:
    mock_page = MagicMock()
    mock_btn = MagicMock()
    mock_btn.count.return_value = 0
    mock_page.locator.return_value = mock_btn

    handle_sso_if_needed(mock_page, timeout=5.0)

    mock_page.wait_for_selector.assert_not_called()


def test_select_per_page_500() -> None:
    mock_page = MagicMock()
    with patch("time.sleep") as mock_sleep:
        select_per_page_500(mock_page, delay=2.0)

    mock_page.select_option.assert_called_once_with("#per-page-filter", "500")
    mock_sleep.assert_called_once_with(2.0)


def test_find_and_click_workflow_match() -> None:
    mock_page = MagicMock()
    mock_row1 = MagicMock()
    mock_link1 = MagicMock()
    mock_link1.count.return_value = 1
    mock_link1.inner_text.return_value = (
        "report-upload-BLINKIT-1102-274-PURCHASE_ORDERS"
    )
    mock_row1.locator.return_value.first = mock_link1

    mock_row2 = MagicMock()
    mock_link2 = MagicMock()
    mock_link2.count.return_value = 1
    mock_link2.inner_text.return_value = (
        "report-upload-AMAZONNOW-1216-1347-SALES"
    )
    mock_row2.locator.return_value.first = mock_link2

    mock_page.locator.return_value.all.return_value = [mock_row1, mock_row2]

    brand = BrandItem(brand="1216", platform="AMAZONNOW")
    matched = find_and_click_workflow(mock_page, [brand])

    assert matched == "report-upload-AMAZONNOW-1216-1347-SALES"
    mock_link2.click.assert_called_once()
    mock_link1.click.assert_not_called()


def test_find_and_click_workflow_no_match() -> None:
    mock_page = MagicMock()
    mock_row = MagicMock()
    mock_link = MagicMock()
    mock_link.count.return_value = 1
    mock_link.inner_text.return_value = "report-upload-BLINKIT-1102-274"
    mock_row.locator.return_value.first = mock_link
    mock_page.locator.return_value.all.return_value = [mock_row]

    brand = BrandItem(brand="1216", platform="AMAZONNOW")
    matched = find_and_click_workflow(mock_page, [brand])

    assert matched is None
    mock_link.click.assert_not_called()


@patch("auto.orchestrator.send_workflow_signal")
@patch("auto.orchestrator.find_and_click_workflow")
@patch("auto.orchestrator.select_per_page_500")
@patch("auto.orchestrator.handle_sso_if_needed")
@patch("time.sleep")
def test_run_orchestrator(
    mock_sleep: MagicMock,
    mock_sso: MagicMock,
    mock_select: MagicMock,
    mock_find: MagicMock,
    mock_signal: MagicMock,
) -> None:
    mock_page = MagicMock()
    settings = Settings(orchestrator_delay=1.0, sso_timeout=10.0)
    brand = BrandItem(brand="1216", platform="AMAZONNOW")
    mock_find.return_value = "report-upload-AMAZONNOW-1216-1347-SALES"

    result = run_orchestrator(mock_page, [brand], settings)

    assert result == "report-upload-AMAZONNOW-1216-1347-SALES"
    mock_page.goto.assert_called_once_with(
        settings.orchestrator_url, wait_until="domcontentloaded"
    )
    mock_sso.assert_called_once_with(mock_page, 10.0)
    mock_select.assert_called_once_with(mock_page, 1.0)
    mock_find.assert_called_once_with(mock_page, [brand])
    mock_signal.assert_called_once_with(mock_page, post_signal_delay=1.0)


@patch("auto.orchestrator.send_workflow_signal")
@patch("auto.orchestrator.find_and_click_workflow")
@patch("auto.orchestrator.select_per_page_500")
@patch("auto.orchestrator.handle_sso_if_needed")
@patch("time.sleep")
def test_run_orchestrator_no_match(
    mock_sleep: MagicMock,
    mock_sso: MagicMock,
    mock_select: MagicMock,
    mock_find: MagicMock,
    mock_signal: MagicMock,
) -> None:
    mock_page = MagicMock()
    settings = Settings(orchestrator_delay=1.0)
    mock_find.return_value = None

    result = run_orchestrator(mock_page, [], settings)

    assert result is None
    mock_signal.assert_not_called()
