# Firstwatch Automation (`auto`)

Playwright automation for [Firstwatch](https://firstwatch.dcluttr.ai/) to automatically resolve 1P City Mapping Errors.

## Workflow
1. Navigates to `https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors`.
2. Preserves persistent browser session in `.auth/profile` (with automatic re-login if needed).
3. Enforces a 3.0-second SPA loading delay.
4. Clicks the **Cities** tab and inspects the error count badge.
5. If errors > 0:
   - Selects the **Select all** checkbox.
   - Clicks **Resolve all** to open the modal.
   - Clicks **Suggest with AI** and waits 5 seconds for suggestions.
   - Detects the enabled **Resolve N cities** button ($N > 0$), clicks it to submit resolution, and waits at least 10 seconds for backend changes to settle.
6. Closes the browser and exits automatically.

## Getting Started

### Installation
Make sure you have [uv](https://docs.astral.sh/uv/) installed.

```powershell
uv sync
```

### Running the Automation
Execute the automated runner:

```powershell
uv run auto
```

Or via the Python module:

```powershell
uv run python -m auto
```

## Configuration
Options can be configured via environment variables or a `.env` file:

| Variable | Default | Description |
|---|---|---|
| `FIRSTWATCH_BASE_URL` | `https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors` | Target URL |
| `FIRSTWATCH_LOGIN_URL` | `https://firstwatch.dcluttr.ai/login` | Login page URL |
| `FIRSTWATCH_EMAIL` | `kshitiz@dcluttr.ai` | Sign-in email address |
| `FIRSTWATCH_PASSWORD` | `dev@123456` | Sign-in password |
| `FIRSTWATCH_NAV_DELAY` | `3.0` | Navigation pause in seconds |
| `FIRSTWATCH_POST_RESOLVE_DELAY` | `10.0` | Post-resolve wait in seconds |
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
