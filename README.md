# Orb Weaver Tools

Utilities for stealth-oriented scraping workflows: Selenium driver setup, rotating headers, proxy support, and browser interaction helpers.

## Features

- `OrbDriver` Selenium bootstrap with optional PIA VPN support
- Spoofed requests with rotating headers and optional proxies
- Proxy harvesting and validation helpers
- Human-like browser interaction utilities
- CLI for common actions (`orb version`, `orb user-agent`, `orb spoof-request`)
- Retry/backoff for network calls

## Installation

Base package:

```bash
pip install orbweaver-tools
```

With Selenium support:

```bash
pip install "orbweaver-tools[selenium]"
```

With scraping table/proxy parsing support:

```bash
pip install "orbweaver-tools[scraping]"
```

Everything:

```bash
pip install "orbweaver-tools[all]"
```

## Quick Start

```python
from orb.config import OrbConfig
from orb.scraper.utils import spoof_request

config = OrbConfig.from_env()
response = spoof_request("https://example.com", config=config)
print(response.status_code)
```

## CLI

```bash
orb version
orb user-agent
orb spoof-request https://example.com --no-proxy
orb proxy-test http://1.2.3.4:8080 https://1.2.3.4:8080
```

## Environment Variables

- `ORB_REQUEST_TIMEOUT` (default: `15`)
- `ORB_MAX_RETRIES` (default: `3`)
- `ORB_BACKOFF_SECONDS` (default: `0.5`)
- `ORB_USE_PROXIES` (`true`/`false`, default: `true`)
- `ORB_USE_USER_AGENT` (`true`/`false`, default: `true`)

## Development

```bash
poetry install --with dev --all-extras
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry run bandit -q -r orb -x orb/common/vpn,orb/common/design,orb/spinner -s B311,B404,B603,B110
poetry run pip-audit
```

## Release

1. Bump version in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Build and publish:

```bash
poetry build
poetry publish --build
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).

## Responsible Use

Only run scraping/automation against systems where you are authorized to do so.
