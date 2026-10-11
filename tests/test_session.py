from unittest.mock import MagicMock, patch

import pytest

from auto.config import Settings
from auto.models import BrandItem
from auto.session import FirstwatchSession


def test_session_uninitialized_page_raises() -> None:
    session = FirstwatchSession()
    with pytest.raises(RuntimeError, match="Session not started"):
        _ = session.page


def test_session_navigate_uninitialized_raises() -> None:
    session = FirstwatchSession()
    with pytest.raises(RuntimeError, match="Session not started"):
        session.navigate("https://firstwatch.dcluttr.ai/")


@patch("auto.session.launch_browser_context")
@patch("auto.session.sync_playwright")
def test_session_start_and_close(
    mock_sync_playwright: MagicMock,
    mock_launch_context: MagicMock,
) -> None:
    mock_pw_instance = MagicMock()
    mock_sync_playwright.return_value.start.return_value = mock_pw_instance

    mock_context = MagicMock()
    mock_page = MagicMock()
    mock_page.url = (
        "https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors"
    )
    locator = MagicMock()
    locator.is_visible.return_value = False
    mock_page.locator.return_value = locator
    mock_context.pages = [mock_page]
    mock_launch_context.return_value = mock_context

    settings = Settings(nav_delay=0.0)
    session = FirstwatchSession(settings)
    page = session.start()

    assert page == mock_page
    mock_page.goto.assert_called_with(
        settings.base_url, wait_until="domcontentloaded"
    )

    session.close()
    mock_context.close.assert_called_once()
    mock_pw_instance.stop.assert_called_once()


@patch("auto.session.suggest_and_resolve")
@patch("auto.session.select_cities_and_open_modal")
def test_session_resolve_city_errors(
    mock_select: MagicMock,
    mock_suggest: MagicMock,
) -> None:
    session = FirstwatchSession()
    session._page = MagicMock()

    brand = BrandItem(brand="1216", platform="AMAZONNOW")
    mock_select.return_value = (True, [brand])
    mock_suggest.return_value = 2

    brands, count = session.resolve_city_errors()
    assert brands == [brand]
    assert count == 2
    mock_select.assert_called_once_with(session.page)
    mock_suggest.assert_called_once_with(
        session.page, session.settings.post_resolve_delay
    )


@patch("auto.session.select_cities_and_open_modal")
def test_session_resolve_city_errors_not_ok(mock_select: MagicMock) -> None:
    session = FirstwatchSession()
    session._page = MagicMock()

    mock_select.return_value = (False, [])

    brands, count = session.resolve_city_errors()
    assert brands == []
    assert count == 0
