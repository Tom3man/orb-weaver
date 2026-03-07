# Contributing

## Setup

```bash
poetry install --with dev --all-extras
pre-commit install
```

## Quality Gates

```bash
poetry run ruff check .
poetry run mypy
poetry run pytest
poetry run bandit -q -r orb -x orb/common/vpn,orb/common/design,orb/spinner -s B311,B404,B603,B110
```

## Release Checklist

1. Update version in `pyproject.toml`.
2. Add changelog entry in `CHANGELOG.md`.
3. Ensure CI is green.
4. Create a release tag.
