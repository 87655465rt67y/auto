from unittest.mock import MagicMock

from auto.auth import is_login_page, login
from auto.config import Settings


def test_is_login_page_via_url() -> None:
    mock_page = MagicMock()
    mock_page.url = "https://firstwatch.dcluttr.ai/login"
    assert is_login_page(mock_page) is True


def test_is_login_page_via_locator() -> None:
    mock_page = MagicMock()
    mock_page.url = "https://firstwatch.dcluttr.ai/"
    locator = MagicMock()
    locator.is_visible.return_value = True
    mock_page.locator.return_value = locator

    assert is_login_page(mock_page) is True
    mock_page.locator.assert_called_with("#email")


def test_is_not_login_page() -> None:
    mock_page = MagicMock()
    mock_page.url = "https://firstwatch.dcluttr.ai/dashboard"
    locator = MagicMock()
    locator.is_visible.return_value = False
    mock_page.locator.return_value = locator

    assert is_login_page(mock_page) is False


def test_login_submits_form() -> None:
    mock_page = MagicMock()
    # First call url is login, second call is dashboard
    mock_page.url = "https://firstwatch.dcluttr.ai/login"
    locator = MagicMock()
    locator.is_visible.return_value = False
    mock_page.locator.return_value = locator

    settings = Settings(email="user@test.com", password="pwd", nav_delay=0.0)

    # After filling/clicking, page url changes
    def mock_click(_selector: str) -> None:
        mock_page.url = "https://firstwatch.dcluttr.ai/dashboard"

    mock_page.click.side_effect = mock_click

    success = login(mock_page, settings)

    mock_page.fill.assert_any_call("#email", "user@test.com")
    mock_page.fill.assert_any_call("#password", "pwd")
    mock_page.click.assert_called_with('button[type="submit"]')
    assert success is True
