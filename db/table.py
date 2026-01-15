# db/table.py

from db.types import TypeSystem

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
        self.indexes = {
            col.name: {} for col in columns if col.unique
        }

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError("Column count mismatch")

        row = {}
        for col, raw in zip(self.columns, values):
            value = TypeSystem.cast(raw, col.dtype)
            row[col.name] = value

        self._enforce_constraints(row)
        self._insert_row(row)

    def _enforce_constraints(self, row):
        for col_name, index in self.indexes.items():
            value = row[col_name]
            if value in index:
                raise ValueError(
                    f"Constraint violation on '{col_name}'"
                )

    def _insert_row(self, row):
        row_id = len(self.rows)
        self.rows.append(row)

        for col_name, index in self.indexes.items():
            index[row[col_name]] = row_id
    
    def filter_rows(self, col_name, value):
    # Use index if exists
        if col_name in self.indexes:
            row_id = self.indexes[col_name].get(value)
            if row_id is not None:
                return [self.rows[row_id]]
            return []
    # fallback: scan all rows
        return [row for row in self.rows if row.get(col_name) == value]

# ✔ Stores rows in memory
# ✔ Casts values to correct types
# ✔ Enforces UNIQUE constraints
# ✔ Uses indexes for efficiency
# ✔ Mimics real database behavior

# rows → actual table data

# indexes → “do we already have this value?”

# insert() → validate → cast → check → save