from unittest.mock import MagicMock, patch

from auto.config import Settings
from auto.main import main, run
from auto.models import BrandItem


@patch("auto.main.run_orchestrator")
@patch("auto.main.FirstwatchSession")
def test_run_with_brands_calls_orchestrator(
    mock_session_cls: MagicMock,
    mock_run_orchestrator: MagicMock,
) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_page = MagicMock()
    mock_page.url = "https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors"
    mock_session.start.return_value = mock_page
    mock_session.page = mock_page

    brand = BrandItem(brand="1216", platform="AMAZONNOW")
    mock_session.resolve_city_errors.return_value = ([brand], 2)
    mock_run_orchestrator.return_value = (
        "report-upload-AMAZONNOW-1216-1347-SALES"
    )

    custom_settings = Settings(nav_delay=0.0)
    mock_session.settings = custom_settings
    resolved = run(custom_settings)

    assert resolved == 2
    mock_session_cls.assert_called_once_with(custom_settings)
    mock_session.start.assert_called_once()
    mock_session.resolve_city_errors.assert_called_once()
    mock_run_orchestrator.assert_called_once_with(
        mock_page, [brand], custom_settings
    )
    mock_session.close.assert_called_once()


@patch("auto.main.run_orchestrator")
@patch("auto.main.FirstwatchSession")
def test_run_without_brands_skips_orchestrator(
    mock_session_cls: MagicMock,
    mock_run_orchestrator: MagicMock,
) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_page = MagicMock()
    mock_session.start.return_value = mock_page
    mock_session.resolve_city_errors.return_value = ([], 0)

    resolved = run()
    assert resolved == 0
    mock_run_orchestrator.assert_not_called()
    mock_session.close.assert_called_once()


@patch("auto.main.run")
def test_main_calls_run(mock_run: MagicMock) -> None:
    main()
    mock_run.assert_called_once_with()
