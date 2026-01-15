# db/engine.py

from db.table import Table
from db.storage import save_table, load_tables

class Database:
    def __init__(self):
        self.tables = load_tables()

    def create_table(self, name, columns):
        if name in self.tables:
            raise ValueError("Table already exists")

        primary_keys = [c for c in columns if c.primary_key]
        if len(primary_keys) > 1:
            raise ValueError("Only one primary key allowed")

        table = Table(name, columns)
        self.tables[name] = table
        save_table(table)

    def insert(self, table_name, values):
        if table_name not in self.tables:
            raise ValueError("Table does not exist")

        table = self.tables[table_name]
        table.insert(values)
        save_table(table)

    def select_all(self, table_name):
        if table_name not in self.tables:
            raise ValueError("Table does not exist")
        return self.tables[table_name].rows
