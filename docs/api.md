# API Overview

## Core Modules

- `orb.config` - runtime configuration model
- `orb.net` - request retry/backoff helper
- `orb.scraper.utils` - spoofed request helper
- `orb.spinner.core.driver` - Selenium driver wrapper
- `orb.logging_utils` - logging setup helper

## Main Entry Points

- `OrbConfig.from_env()`
- `spoof_request(...)`
- `OrbDriver(...).get_webdriver(...)`
- `setup_logging(...)`
