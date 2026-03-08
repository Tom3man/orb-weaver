# API Overview

## `sqlite_forge.SqliteDatabase`

Main entry point for schema-driven table management.

Useful methods:

- `create_table(overwrite=False)`
- `drop_table()`
- `exists()`
- `ingest_dataframe(df, load_date=False, overwrite=False)`
- `execute_query(query)`
- `fetch_table(limit=None)`
- `export_table(output_path, format="csv", limit=None)`
