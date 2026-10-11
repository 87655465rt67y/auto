from pathlib import Path

from auto.config import Settings, get_settings


def test_settings_defaults() -> None:
    settings = get_settings()
    assert (
        settings.base_url
        == "https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors"
    )
    assert settings.login_url == "https://firstwatch.dcluttr.ai/login"
    assert settings.email == "kshitiz@dcluttr.ai"
    assert settings.password == "dev@123456"
    assert settings.nav_delay == 3.0
    assert settings.post_resolve_delay == 10.0
    assert (
        settings.orchestrator_url
        == "https://orchestrator.dcluttr.ai/namespaces/default/workflows"
    )
    assert settings.sso_timeout == 60.0
    assert settings.orchestrator_delay == 5.0
    assert settings.profile_dir == Path(".auth/profile")
    assert settings.headless is False


def test_custom_settings() -> None:
    settings = Settings(
        email="test@example.com",
        password="secret",
        nav_delay=5.0,
        post_resolve_delay=15.0,
        orchestrator_url="https://custom.orchestrator.ai",
        sso_timeout=30.0,
        orchestrator_delay=2.0,
        headless=True,
    )
    assert settings.email == "test@example.com"
    assert settings.password == "secret"
    assert settings.nav_delay == 5.0
    assert settings.post_resolve_delay == 15.0
    assert settings.orchestrator_url == "https://custom.orchestrator.ai"
    assert settings.sso_timeout == 30.0
    assert settings.orchestrator_delay == 2.0
    assert settings.headless is True
