# db/schema.py

class Column:
    def __init__(self, name, dtype, primary_key=False, unique=False):
        self.name = name
        self.dtype = dtype
        self.primary_key = primary_key
        self.unique = unique or primary_key
