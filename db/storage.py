# db/storage.py

import json
import os
from db.schema import Column
from db.table import Table

DATA_DIR = "data"

def save_table(table):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{table.name}.json")

    data = {
        "name": table.name,
        "columns": [
            {
                "name": c.name,
                "dtype": c.dtype,
                "primary_key": c.primary_key,
                "unique": c.unique
            }
            for c in table.columns
        ],
        "rows": table.rows,
        "indexes": table.indexes
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_tables():
    tables = {}

    if not os.path.exists(DATA_DIR):
        return tables

    for file in os.listdir(DATA_DIR):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(DATA_DIR, file)) as f:
            data = json.load(f)

        columns = [
            Column(
                c["name"],
                c["dtype"],
                c["primary_key"],
                c["unique"]
            )
            for c in data["columns"]
        ]

        table = Table(data["name"], columns)
        table.rows = data["rows"]
        table.indexes = data["indexes"]
        tables[table.name.lower()] = table

    return tables
