from unittest.mock import MagicMock, patch

from auto.config import Settings
from auto.main import main, run


@patch("auto.main.FirstwatchSession")
def test_run_executes_and_closes_session(mock_session_cls: MagicMock) -> None:
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    mock_page = MagicMock()
    mock_page.url = "https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors"
    mock_session.start.return_value = mock_page
    mock_session.resolve_city_errors.return_value = 2

    custom_settings = Settings(nav_delay=0.0)
    resolved = run(custom_settings)

    assert resolved == 2
    mock_session_cls.assert_called_once_with(custom_settings)
    mock_session.start.assert_called_once()
    mock_session.resolve_city_errors.assert_called_once()
    mock_session.close.assert_called_once()


@patch("auto.main.run")
def test_main_calls_run(mock_run: MagicMock) -> None:
    main()
    mock_run.assert_called_once_with()
