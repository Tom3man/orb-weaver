# Contributing

## Local Checks

```bash
poetry run ruff check .
poetry run mypy
poetry run pytest
poetry run bandit -q -r orb -x orb/common/vpn,orb/common/design,orb/spinner -s B311,B404,B603,B110
```

## Build Docs Locally

```bash
poetry run mkdocs serve
```

Then open `http://127.0.0.1:8000`.
