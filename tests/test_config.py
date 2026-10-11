from pathlib import Path

from auto.config import Settings, get_settings


def test_settings_defaults() -> None:
    settings = get_settings()
    assert settings.base_url == "https://firstwatch.dcluttr.ai/"
    assert settings.login_url == "https://firstwatch.dcluttr.ai/login"
    assert settings.email == "kshitiz@dcluttr.ai"
    assert settings.password == "dev@123456"
    assert settings.nav_delay == 3.0
    assert settings.profile_dir == Path(".auth/profile")
    assert settings.headless is False


def test_custom_settings() -> None:
    settings = Settings(
        email="test@example.com",
        password="secret",
        nav_delay=5.0,
        headless=True,
    )
    assert settings.email == "test@example.com"
    assert settings.password == "secret"
    assert settings.nav_delay == 5.0
    assert settings.headless is True
