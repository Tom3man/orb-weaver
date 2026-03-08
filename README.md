# SQLite Forge

SQLite Forge is a lightweight toolkit that helps you declare and maintain SQLite tables from Python. Define your schema once, then manage tables, run queries, ingest pandas `DataFrame` objects, and export results.

## Highlights

- Declarative table definitions with schemas and optional multi-column primary keys
- Safe helpers to create/drop tables and check existence
- DataFrame ingestion with optional incremental overwrite support
- Query execution that returns pandas `DataFrame` objects
- Table export helpers for `csv`, `json`, and `parquet`

## Installation

```bash
pip install sqlite-forge
```

For development:

```bash
git clone https://github.com/Tom3man/sqlite-forge.git
cd sqlite-forge
poetry install --with dev --with docs
```

## Quick Start

```python
from pathlib import Path

import pandas as pd

from sqlite_forge import SqliteDatabase


class ExampleTable(SqliteDatabase):
    DEFAULT_PATH = "example_table"
    PRIMARY_KEY = ("id",)
    DEFAULT_SCHEMA = {
        "id": "INTEGER",
        "name": "TEXT",
        "score": "REAL",
    }


db = ExampleTable(database_path=Path("./data"))
db.create_table(overwrite=True)

db.ingest_dataframe(
    pd.DataFrame(
        [
            {"id": 1, "name": "Alice", "score": 9.2},
            {"id": 2, "name": "Bob", "score": 8.7},
        ]
    )
)

print(db.fetch_table())
db.export_table("./data/example_table.csv", format="csv")
```

## Development

```bash
poetry run pytest
poetry run ruff check .
poetry run mypy
poetry build
```

## Documentation

- Docs site: https://tom3man.github.io/sqlite-forge/
- Build locally:

```bash
poetry run mkdocs serve
```

## Release

1. Bump version in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Publish:

```bash
poetry publish --build
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Licence

MIT. See [LICENSE](LICENSE).
