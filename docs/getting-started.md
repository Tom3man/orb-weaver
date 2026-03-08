# Getting Started

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
db.ingest_dataframe(pd.DataFrame([{"id": 1, "name": "Alice", "score": 9.2}]))
print(db.fetch_table())
db.export_table("./data/example_table.csv", format="csv")
```
