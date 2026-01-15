from db.table import Table
from db.storage import save_table, load_tables

class Database:
    def __init__(self):
        # load tables, normalize keys to lowercase
        loaded = load_tables()
        self.tables = {name.lower(): table for name, table in loaded.items()}

    def create_table(self, name, columns):
        name = name.lower()   # normalize
        if name in self.tables:
            raise ValueError("Table already exists")

        primary_keys = [c for c in columns if c.primary_key]
        if len(primary_keys) > 1:
            raise ValueError("Only one primary key allowed")

        table = Table(name, columns)
        self.tables[name] = table
        save_table(table)

    def insert(self, table_name, values):
        table_name = table_name.lower()
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        table = self.tables[table_name]
        table.insert(values)
        save_table(table)

    def select_all(self, table_name):
        table_name = table_name.lower()
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        return self.tables[table_name].rows

    def select_where(self, table_name, col, val):
        table_name = table_name.lower()
        table = self.tables[table_name]
        return table.filter_rows(col, val)

    def update(self, table_name, set_col, set_val, where_col, where_val):
        table_name = table_name.lower()
        table = self.tables[table_name]
        table.update_rows(set_col, set_val, where_col, where_val)
        save_table(table)

    def delete(self, table_name, where_col, where_val):
        table_name = table_name.lower()
        table = self.tables[table_name]
        table.delete_rows(where_col, where_val)
        save_table(table)
