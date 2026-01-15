def parse_select(sql):
    sql = sql.rstrip(";")
    table_part = sql.split("FROM")[1].strip()
    if "WHERE" in table_part.upper():
        table_name, where_part = table_part.upper().split("WHERE")
        table_name = table_name.strip().lower()
        where_part = where_part.strip()
        # support single condition: column = value
        col, val = where_part.split("=")
        col = col.strip()
        val = val.strip().strip("'")
        if val.isdigit():
            val = int(val)
        return ("SELECT_WHERE", table_name, col, val)
    else:
        table_name = table_part.strip().lower()
        return ("SELECT", table_name)

def parse_update(sql):
    sql = sql.rstrip(";")
    table_name = sql.split()[1].lower()
    set_part = sql.split("SET")[1].split("WHERE")[0].strip()
    col, val = set_part.split("=")
    col = col.strip()
    val = val.strip().strip("'")
    if val.isdigit():
        val = int(val)
    where_part = sql.split("WHERE")[1].strip()
    where_col, where_val = where_part.split("=")
    where_col = where_col.strip()
    where_val = where_val.strip().strip("'")
    if where_val.isdigit():
        where_val = int(where_val)
    return ("UPDATE", table_name, col, val, where_col, where_val)


def parse_delete(sql):
    sql = sql.rstrip(";")
    table_name = sql.split()[2].lower()
    where_part = sql.split("WHERE")[1].strip()
    col, val = where_part.split("=")
    col = col.strip()
    val = val.strip().strip("'")
    if val.isdigit():
        val = int(val)
    return ("DELETE", table_name, col, val)
