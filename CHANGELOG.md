# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [1.2.0] - 2026-03-07

### Added

- CLI entrypoint (`orb`) for version, user-agent generation, spoofed requests, and proxy testing.
- Runtime config model (`OrbConfig`) with environment variable support.
- Logging setup helper (`setup_logging`) for package consumers.
- Network retry helper with exponential backoff.
- Tooling and quality configuration for `ruff`, `mypy`, `bandit`, `pip-audit`, and coverage.
- Pre-commit configuration and examples.
- CI hardening for lint/type/security/test/build checks.

### Changed

- Updated package distribution name to `orbweaver-tools`.
- Improved request reliability in scraping/proxy modules via retries and timeout handling.

## [1.1.0] - 2025-10-18

### Added

- Initial public release metadata and packaging support.
