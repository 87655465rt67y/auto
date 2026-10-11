from auto.config import Settings
from auto.session import FirstwatchSession


def run(settings: Settings | None = None) -> int:
    """Execute Firstwatch automation workflow and exit."""
    session = FirstwatchSession(settings)
    try:
        session.start()
        print(f"Connected to Firstwatch: {session.page.url}")
        resolved = session.resolve_city_errors()
        if resolved > 0:
            print(f"Successfully resolved {resolved} cities mapping error(s).")
        else:
            print("No city mapping errors needed resolution.")
        return resolved
    finally:
        session.close()
        print("Browser closed. Automation finished.")


def main() -> None:
    run()
