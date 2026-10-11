from unittest.mock import MagicMock

from auto.cli import handle_command


def test_handle_command_empty() -> None:
    session = MagicMock()
    assert handle_command(session, "   ") is True
    session.navigate.assert_not_called()


def test_handle_command_exit() -> None:
    session = MagicMock()
    assert handle_command(session, "exit") is False
    assert handle_command(session, "quit") is False
    assert handle_command(session, "q") is False


def test_handle_command_goto() -> None:
    session = MagicMock()
    session.page.url = "https://firstwatch.dcluttr.ai/settings"
    assert handle_command(session, "goto https://firstwatch.dcluttr.ai/settings") is True
    session.navigate.assert_called_with("https://firstwatch.dcluttr.ai/settings")


def test_handle_command_reload() -> None:
    session = MagicMock()
    session.page.url = "https://firstwatch.dcluttr.ai/warehouses"
    assert handle_command(session, "reload") is True
    session.navigate.assert_called_with("https://firstwatch.dcluttr.ai/warehouses")


def test_handle_command_url(capsys: object) -> None:
    session = MagicMock()
    session.page.url = "https://firstwatch.dcluttr.ai/home"
    assert handle_command(session, "url") is True
