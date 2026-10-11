from auto.config import Settings
from auto.orchestrator import run_orchestrator
from auto.session import FirstwatchSession


def run(settings: Settings | None = None) -> int:
    """Execute Firstwatch and Orchestrator automation workflow."""
    session = FirstwatchSession(settings)
    try:
        session.start()
        print(f"Connected to Firstwatch: {session.page.url}")
        brands, resolved = session.resolve_city_errors()
        print(f"Resolved {resolved} error(s). Brands: {[b.brand for b in brands]}")
        if brands:
            print(f"Navigating to Orchestrator with {len(brands)} brand(s)...")
            matched = run_orchestrator(session.page, brands, session.settings)
            print(f"Selected workflow: {matched}")
        return resolved
    finally:
        session.close()
        print("Browser closed. Automation finished.")


def main() -> None:
    run()
