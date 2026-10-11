# Firstwatch & Orchestrator Automation (`auto`)

Playwright automation for [Firstwatch](https://firstwatch.dcluttr.ai/) and [Orchestrator](https://orchestrator.dcluttr.ai/) to automatically resolve 1P City Mapping Errors, locate matching workflows, and send the `retry_upload` signal.

## Workflow

### Phase 1: Firstwatch Resolution & Brand Extraction
1. Navigates to `https://firstwatch.dcluttr.ai/data/data-upload/1p-mapping-errors`.
2. Preserves persistent browser session in `.auth/profile` (with automatic re-login if needed).
3. Enforces a 3.0-second SPA loading delay.
4. Clicks the **Cities** tab and inspects the error count badge.
5. If errors > 0:
   - Selects the **Select all** checkbox.
   - Extracts all selected **Brand** and **Platform** items (e.g. brand `1216` and platform `AMAZONNOW`).
   - Clicks **Resolve all** to open the modal.
   - Clicks **Suggest with AI** and waits 5 seconds for suggestions.
   - Detects the enabled **Resolve N cities** button ($N > 0$), clicks it to submit resolution, and waits at least 10 seconds for backend changes to settle.

### Phase 2: Orchestrator Workflow Matching & Signal Trigger
6. Navigates to `https://orchestrator.dcluttr.ai/namespaces/default/workflows` and waits 5 seconds.
7. Detects the **Continue to SSO** button if present; if found, clicks it and waits up to 60 seconds for Google SSO sign-in.
8. Selects **500** in the `#per-page-filter` dropdown and pauses 5 seconds for rows to reload.
9. Iterates through the extracted brands array from top to bottom, matches the first workflow whose ID contains the brand (e.g. `report-upload-AMAZONNOW-1216-1347-SALES`), and clicks on it.
10. Waits 5 seconds for the workflow page to load.
11. Clicks **More Actions**, then clicks **Send a Signal**, and waits 2 seconds for the confirmation modal to open.
12. Clicks the **Signal name** selector, selects **`retry_upload`**, and clicks **Submit**.
13. Waits 5 seconds for signal transmission, closes the browser, and exits automatically.

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
| `ORCHESTRATOR_URL` | `https://orchestrator.dcluttr.ai/namespaces/default/workflows` | Orchestrator workflows URL |
| `ORCHESTRATOR_SSO_TIMEOUT` | `60.0` | Google SSO wait timeout in seconds |
| `ORCHESTRATOR_DELAY` | `5.0` | Orchestrator loading pause in seconds |
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
