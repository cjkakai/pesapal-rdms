from db.engine import Database
from db.schema import Column

db = Database()

print("Pesapal RDBMS — Step 3")
print("Type EXIT to quit")

while True:
    try:
        sql = input("db> ").strip()
        if sql.upper() == "EXIT":
            break

        sql_upper = sql.upper()

        # ---------------- CREATE TABLE ----------------
        if sql_upper.startswith("CREATE TABLE"):
            name = sql.split()[2].lower().strip(" ;")
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

        # ---------------- INSERT INTO ----------------
        elif sql_upper.startswith("INSERT INTO"):
            table = sql.split()[2].lower().strip(" ;")
            values = sql[sql.index("(")+1 : sql.rindex(")")]
            parsed = []

            for v in values.split(","):
                v = v.strip().strip(";")
                if v.startswith("'") and v.endswith("'"):
                    parsed.append(v.strip("'"))
                elif v.isdigit():
                    parsed.append(int(v))
                else:
                    parsed.append(v)

            db.insert(table, parsed)
            print("Row inserted")

        # ---------------- SELECT ----------------
        elif sql_upper.startswith("SELECT"):
            if "WHERE" in sql_upper:
                # SELECT * FROM users WHERE id = 1;
                parts = sql.split("WHERE")
                table = parts[0].split()[-1].lower().strip(" ;")
                cond = parts[1].strip().rstrip(";")
                col, val = cond.split("=")
                col = col.strip()
                val = val.strip().strip("'")
                if val.isdigit():
                    val = int(val)
                rows = db.select_where(table, col, val)
            else:
                table = sql.split()[-1].lower().strip(" ;")
                rows = db.select_all(table)

            for r in rows:
                print(r)

        # ---------------- UPDATE ----------------
        elif sql_upper.startswith("UPDATE"):
            # UPDATE users SET name = 'Bob' WHERE id = 2;
            table = sql.split()[1].lower().strip(" ;")
            set_part = sql.split("SET")[1].split("WHERE")[0].strip()
            set_col, set_val = set_part.split("=")
            set_col = set_col.strip()
            set_val = set_val.strip().strip("'").strip(";")
            if set_val.isdigit():
                set_val = int(set_val)

            where_part = sql.split("WHERE")[1].strip().rstrip(";")
            where_col, where_val = where_part.split("=")
            where_col = where_col.strip()
            where_val = where_val.strip().strip("'")
            if where_val.isdigit():
                where_val = int(where_val)

            db.update(table, set_col, set_val, where_col, where_val)
            print("Rows updated")

        # ---------------- DELETE ----------------
        elif sql_upper.startswith("DELETE"):
            # DELETE FROM users WHERE id = 2;
            table = sql.split()[2].lower().strip(" ;")
            where_part = sql.split("WHERE")[1].strip().rstrip(";")
            col, val = where_part.split("=")
            col = col.strip()
            val = val.strip().strip("'")
            if val.isdigit():
                val = int(val)
            db.delete(table, col, val)
            print("Rows deleted")
        
        elif "INNER JOIN" in sql_upper:
            parts = sql_upper.split("INNER JOIN")
            left_table = parts[0].split()[-1].lower().strip(" ;")
            right_part = parts[1].strip()
            right_table = right_part.split("ON")[0].strip().lower()
            on_condition = right_part.split("ON")[1].strip().rstrip(";")
            left_col, right_col = [x.strip() for x in on_condition.split("=")]
            left_col = left_col.split(".")[1]  # remove table prefix
            right_col = right_col.split(".")[1]

            rows = db.inner_join(left_table, right_table, left_col, right_col)
            for r in rows:
                print(r)
        
        else:
            print("Unsupported command")
            
    except Exception as e:
        print("ERROR:", e)
