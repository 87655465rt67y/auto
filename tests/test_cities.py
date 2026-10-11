from unittest.mock import MagicMock, patch

from auto.cities import (
    extract_selected_brands,
    select_cities_and_open_modal,
    suggest_and_resolve,
)
from auto.models import BrandItem


def test_extract_selected_brands() -> None:
    mock_page = MagicMock()
    mock_row1 = MagicMock()
    mock_cb1 = MagicMock()
    mock_cb1.count.return_value = 1
    mock_cb1.get_attribute.return_value = "checked"
    mock_row1.locator.side_effect = lambda sel: (
        mock_cb1
        if "checkbox" in sel
        else MagicMock(
            nth=lambda idx: MagicMock(
                inner_text=lambda: "1216" if idx == 2 else "AMAZONNOW"
            )
        )
    )

    mock_row2 = MagicMock()
    mock_cb2 = MagicMock()
    mock_cb2.count.return_value = 1
    mock_cb2.get_attribute.return_value = "unchecked"
    mock_row2.locator.side_effect = lambda sel: (
        mock_cb2
        if "checkbox" in sel
        else MagicMock(
            nth=lambda idx: MagicMock(
                inner_text=lambda: "9999" if idx == 2 else "BLINKIT"
            )
        )
    )

    mock_page.locator.return_value.all.return_value = [mock_row1, mock_row2]

    brands = extract_selected_brands(mock_page)
    assert len(brands) == 1
    assert brands[0] == BrandItem(brand="1216", platform="AMAZONNOW")


def test_select_cities_zero_errors() -> None:
    mock_page = MagicMock()
    mock_tab = MagicMock()
    mock_badge = MagicMock()
    mock_badge.count.return_value = 1
    mock_badge.inner_text.return_value = "0"
    mock_tab.locator.return_value.first = mock_badge
    mock_page.locator.return_value = mock_tab

    with patch("time.sleep"):
        ok, brands = select_cities_and_open_modal(mock_page)

    assert ok is False
    assert brands == []
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

    mock_row = MagicMock()
    mock_row_cb = MagicMock()
    mock_row_cb.count.return_value = 1
    mock_row_cb.get_attribute.return_value = "checked"
    mock_row.locator.side_effect = lambda sel: (
        mock_row_cb
        if "checkbox" in sel
        else MagicMock(
            nth=lambda idx: MagicMock(
                inner_text=lambda: "1216" if idx == 2 else "AMAZONNOW"
            )
        )
    )
    mock_table_rows = MagicMock()
    mock_table_rows.all.return_value = [mock_row]

    def locator_side_effect(selector: str) -> MagicMock:
        if 'button[role="tab"]' in selector:
            return mock_tab
        if 'button[role="checkbox"][aria-label="Select all"]' in selector:
            return mock_cb
        if "table tbody tr" in selector:
            return mock_table_rows
        if 'button:has-text("Resolve all")' in selector:
            return mock_resolve_all
        return MagicMock()

    mock_page.locator.side_effect = locator_side_effect

    with patch("time.sleep"):
        ok, brands = select_cities_and_open_modal(mock_page)

    assert ok is True
    assert brands == [BrandItem(brand="1216", platform="AMAZONNOW")]
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
