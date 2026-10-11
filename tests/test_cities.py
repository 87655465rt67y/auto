from unittest.mock import MagicMock, patch

from auto.cities import select_cities_and_open_modal, suggest_and_resolve


def test_select_cities_zero_errors() -> None:
    mock_page = MagicMock()
    mock_tab = MagicMock()
    mock_badge = MagicMock()
    mock_badge.count.return_value = 1
    mock_badge.inner_text.return_value = "0"
    mock_tab.locator.return_value.first = mock_badge
    mock_page.locator.return_value = mock_tab

    with patch("time.sleep"):
        result = select_cities_and_open_modal(mock_page)

    assert result is False
    mock_tab.click.assert_called_once()


def test_select_cities_with_errors() -> None:
    mock_page = MagicMock()
    mock_tab = MagicMock()
    mock_badge = MagicMock()
    mock_badge.count.return_value = 1
    mock_badge.inner_text.return_value = "2"
    mock_tab.locator.return_value.first = mock_badge

    mock_cb = MagicMock()
    mock_cb.count.return_value = 1
    mock_cb.get_attribute.return_value = "unchecked"

    mock_resolve_btn = MagicMock()
    mock_resolve_btn.is_enabled.return_value = True
    mock_resolve_all = MagicMock()
    mock_resolve_all.all.return_value = [mock_resolve_btn]

    def locator_side_effect(selector: str) -> MagicMock:
        if 'button[role="tab"]' in selector:
            return mock_tab
        if 'button[role="checkbox"]' in selector:
            return mock_cb
        if 'button:has-text("Resolve all")' in selector:
            return mock_resolve_all
        return MagicMock()

    mock_page.locator.side_effect = locator_side_effect

    with patch("time.sleep"):
        result = select_cities_and_open_modal(mock_page)

    assert result is True
    mock_cb.click.assert_called_once()
    mock_resolve_btn.click.assert_called_once()


def test_suggest_and_resolve_enabled() -> None:
    mock_page = MagicMock()
    mock_dialog = MagicMock()
    mock_suggest_btn = MagicMock()
    mock_resolve_btn = MagicMock()
    mock_resolve_btn.is_enabled.return_value = True
    mock_resolve_btn.inner_text.return_value = "Resolve 2 cities"

    def dialog_locator(selector: str) -> MagicMock:
        if "Suggest with AI" in selector:
            return mock_suggest_btn
        if "Resolve " in selector:
            return mock_resolve_btn
        return MagicMock()

    mock_dialog.locator.side_effect = dialog_locator
    mock_page.locator.return_value = mock_dialog

    with patch("time.sleep") as mock_sleep:
        resolved = suggest_and_resolve(mock_page, post_resolve_delay=12.0)

    assert resolved == 2
    mock_suggest_btn.click.assert_called_once()
    mock_resolve_btn.click.assert_called_once()
    mock_sleep.assert_any_call(12.0)


def test_suggest_and_resolve_disabled() -> None:
    mock_page = MagicMock()
    mock_dialog = MagicMock()
    mock_suggest_btn = MagicMock()
    mock_resolve_btn = MagicMock()
    mock_resolve_btn.is_enabled.return_value = False
    mock_resolve_btn.inner_text.return_value = "Resolve 0 cities"

    def dialog_locator(selector: str) -> MagicMock:
        if "Suggest with AI" in selector:
            return mock_suggest_btn
        if "Resolve " in selector:
            return mock_resolve_btn
        return MagicMock()

    mock_dialog.locator.side_effect = dialog_locator
    mock_page.locator.return_value = mock_dialog

    with patch("time.sleep"):
        resolved = suggest_and_resolve(mock_page)

    assert resolved == 0
    mock_suggest_btn.click.assert_called_once()
    mock_resolve_btn.click.assert_not_called()
