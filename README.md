# Orb Weaver

Utilities for stealth-oriented web scraping with Selenium helpers, rotating headers, and proxy support.

## Features

- Selenium driver bootstrap via `OrbDriver`
- Randomized user-agent and request headers
- Proxy harvesting and validation utilities
- Human-like browser interaction helpers (`slow_type`, random clicking, scroll, viewport changes)
- Optional PIA VPN integration for IP rotation

## Installation

From PyPI (after publish):

```bash
pip install orbweaver-tools
```

From source with Poetry:

```bash
poetry install
```

## Quick Start

### Build a Selenium driver

```python
from orb.spinner.core.driver import OrbDriver

orb_driver = OrbDriver(use_pia=False)
driver = orb_driver.get_webdriver(url="https://example.com")
```

### Send spoofed requests

```python
from bs4 import BeautifulSoup
from orb.scraper.utils import spoof_request

response = spoof_request("https://example.com", use_proxies=False)
soup = BeautifulSoup(response.content, "html.parser")
```

### Human-like interactions

```python
from selenium.webdriver.common.by import By
from orb.spinner.utils import slow_type, human_clicking

input_box = driver.find_element(By.ID, "search")
slow_type(input_box, "hello world", send_keys=True)

button = driver.find_element(By.ID, "submit")
human_clicking(driver, button)
```

## Development

Run tests:

```bash
poetry run pytest -q
```

Build package artifacts:

```bash
poetry build
```

## Publish to PyPI

1. Create an account on [PyPI](https://pypi.org/).
2. Create an API token and configure Poetry credentials:

```bash
poetry config pypi-token.pypi <your-token>
```

3. Publish:

```bash
poetry publish --build
```

## License

MIT. See [`LICENSE`](LICENSE).

## Notes

Use these tools responsibly and only against systems where you have permission to automate or scrape.
