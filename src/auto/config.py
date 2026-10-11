from dataclasses import dataclass
from pathlib import Path

from decouple import config


@dataclass(frozen=True)
class Settings:
    base_url: str = config(
        "FIRSTWATCH_BASE_URL",
        default="https://firstwatch.dcluttr.ai/",
    )
    login_url: str = config(
        "FIRSTWATCH_LOGIN_URL",
        default="https://firstwatch.dcluttr.ai/login",
    )
    email: str = config("FIRSTWATCH_EMAIL", default="kshitiz@dcluttr.ai")
    password: str = config("FIRSTWATCH_PASSWORD", default="dev@123456")
    nav_delay: float = config(
        "FIRSTWATCH_NAV_DELAY",
        default=3.0,
        cast=float,
    )
    profile_dir: Path = Path(
        config("FIRSTWATCH_PROFILE_DIR", default=".auth/profile")
    )
    headless: bool = config(
        "FIRSTWATCH_HEADLESS",
        default=False,
        cast=bool,
    )


def get_settings() -> Settings:
    return Settings()
