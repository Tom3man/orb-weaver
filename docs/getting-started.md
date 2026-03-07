# Getting Started

## Install for Development

```bash
poetry install --with dev --all-extras --with docs
```

## First Request

```python
from orb.config import OrbConfig
from orb.scraper.utils import spoof_request

config = OrbConfig.from_env()
response = spoof_request("https://example.com", config=config)
print(response.status_code)
```

## Environment Variables

- `ORB_REQUEST_TIMEOUT`
- `ORB_MAX_RETRIES`
- `ORB_BACKOFF_SECONDS`
- `ORB_USE_PROXIES`
- `ORB_USE_USER_AGENT`
