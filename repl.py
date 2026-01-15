# repl.py

from db.engine import Database
from db.schema import Column

db = Database()

print("Pesapal RDBMS — Step 2")
print("Type EXIT to quit")

while True:
    try:
        sql = input("db> ").strip()
        if sql.upper() == "EXIT":
            break

        if sql.upper().startswith("CREATE TABLE"):
            name = sql.split()[2]
            body = sql[sql.index("(")+1 : sql.rindex(")")]
            cols = []

            for part in body.split(","):
                tokens = part.strip().split()
                col = tokens[0]
                dtype = tokens[1].upper()
                primary = "PRIMARY" in part.upper()
                unique = "UNIQUE" in part.upper()
                cols.append(Column(col, dtype, primary, unique))

            db.create_table(name, cols)
            print("Table created")

        elif sql.upper().startswith("INSERT INTO"):
            table = sql.split()[2]
            values = sql[sql.index("(")+1 : sql.rindex(")")]
            parsed = []

            for v in values.split(","):
                v = v.strip()
                if v.startswith("'"):
                    parsed.append(v.strip("'"))
                else:
                    parsed.append(v)

            db.insert(table, parsed)
            print("Row inserted")

        elif sql.upper().startswith("SELECT"):
            table = sql.split()[-1]
            rows = db.select_all(table)
            for r in rows:
                print(r)

        else:
            print("Unsupported command")

    except Exception as e:
        print("ERROR:", e)
