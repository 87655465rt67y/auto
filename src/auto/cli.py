from auto.session import FirstwatchSession


def handle_command(session: FirstwatchSession, line: str) -> bool:
    """Execute a CLI command. Returns False to exit."""
    cmd = line.strip()
    if not cmd:
        return True
    parts = cmd.split(maxsplit=1)
    action = parts[0].lower()
    if action in ("exit", "quit", "q"):
        return False
    if action == "goto" and len(parts) > 1:
        session.navigate(parts[1])
        print(f"Navigated to: {session.page.url}")
    elif action == "reload":
        session.navigate(session.page.url)
        print("Page reloaded.")
    elif action == "url":
        print(f"Current URL: {session.page.url}")
    else:
        print("Commands: goto <url>, reload, url, exit")
    return True


def run_loop(session: FirstwatchSession) -> None:
    """Keep session alive and handle user commands."""
    print("Session active! Type 'exit' to quit or 'help' for commands.")
    try:
        while True:
            line = input("firstwatch> ")
            if not handle_command(session, line):
                break
    except (KeyboardInterrupt, EOFError):
        print("\nExiting session...")


def main() -> None:
    session = FirstwatchSession()
    try:
        session.start()
        run_loop(session)
    finally:
        session.close()
