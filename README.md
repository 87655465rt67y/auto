# Firstwatch Automation (`auto`)

Playwright automation and persistent session manager for [Firstwatch](https://firstwatch.dcluttr.ai/).

## Features
- **Persistent Session State**: Maintains cookies, tokens, and browser state in `.auth/profile` so you stay logged in across runs.
- **Auto Re-Login Guard**: Detects unauthenticated redirects back to `/login` and automatically re-authenticates.
- **Generous SPA Loading Delay**: Enforces a 3.0-second delay after all navigations and actions to ensure single-page application data renders completely.
- **Interactive Headful CLI**: Keeps the browser window open and active with an interactive prompt for running ad-hoc navigations.
- **NASA JPL Rule 4 Compliant**: All production modules and functions fit on a single printed sheet (≤ 60 lines).

## Getting Started

### Installation
Make sure you have [uv](https://docs.astral.sh/uv/) installed.

```powershell
uv sync
```

### Running the Automation
Launch the headful interactive session:

```powershell
uv run auto
```

Or execute directly via the Python module:

```powershell
uv run python -m auto.cli
```

### CLI Commands
Once the session launches, an interactive prompt will be displayed:
- `goto <url>`: Navigate to any Firstwatch URL (applies 3s load delay and login check).
- `reload`: Reload the current page.
- `url`: Display the current page URL.
- `exit` / `quit`: Close the browser and terminate the session cleanly.

## Configuration
Options can be configured via environment variables or a `.env` file:

| Variable | Default | Description |
|---|---|---|
| `FIRSTWATCH_BASE_URL` | `https://firstwatch.dcluttr.ai/` | Base target URL |
| `FIRSTWATCH_LOGIN_URL` | `https://firstwatch.dcluttr.ai/login` | Login page URL |
| `FIRSTWATCH_EMAIL` | `kshitiz@dcluttr.ai` | Sign-in email address |
| `FIRSTWATCH_PASSWORD` | `dev@123456` | Sign-in password |
| `FIRSTWATCH_NAV_DELAY` | `3.0` | Navigation pause in seconds |
| `FIRSTWATCH_PROFILE_DIR` | `.auth/profile` | Persistent browser profile directory |
| `FIRSTWATCH_HEADLESS` | `False` | Run browser in headless mode |

## Development & Verification Gates
Run all verification gates:

```powershell
uv run ruff check --fix
uv run ty check
uv run python -m pytest
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for architectural details.
