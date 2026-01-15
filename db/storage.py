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
        
        # Fix: Convert index keys back to proper types (JSON converts int keys to strings)
        table.indexes = {}
        for col_name, idx in data["indexes"].items():
            col = next((c for c in columns if c.name == col_name), None)
            if col and col.dtype == "INT":
                table.indexes[col_name] = {int(k): v for k, v in idx.items()}
            else:
                table.indexes[col_name] = idx
        
        tables[table.name.lower()] = table

    return tables
