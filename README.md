# Pesapal RDBMS — Junior Dev Challenge 2026

A mini **relational database management system (RDBMS)** built from scratch in Python for the Pesapal Junior Developer Challenge 2026.  

It demonstrates core database functionality:
- Table creation with INT and TEXT columns
- Primary and UNIQUE constraints
- CRUD operations (INSERT, SELECT, UPDATE, DELETE)
- Basic indexing for fast lookups
- INNER JOINs between tables
- Simple WHERE filters
- Interactive SQL-like REPL
- Persistent JSON storage

---

## 💡 Project Goals

The project was designed to demonstrate:
- Understanding of relational database concepts  
- Ability to implement core RDBMS features from scratch  
- Problem-solving and coding discipline  
- End-to-end project delivery (engine + REPL + demo usage)

---

## ⚙️ Features

### Table Management
```sql
CREATE TABLE users (id INT PRIMARY KEY, email TEXT UNIQUE, name TEXT);
```

### Insert Data
```sql
INSERT INTO users VALUES (1, 'alice@domain.com', 'Alice');
```

### Select Data
```sql
SELECT * FROM users;
SELECT * FROM users WHERE id = 1;
```

### Update & Delete
```sql
UPDATE users SET name = 'Bob' WHERE id = 1;
DELETE FROM users WHERE id = 2;
```

### JOINs
```sql
SELECT * FROM users
INNER JOIN orders ON users.id = orders.user_id
WHERE total > 100;
```

### REPL Commands
- Type `EXIT` to quit
- SQL keywords are case-insensitive
- All errors are human-readable

---

## 🛠️ Architecture Overview

- **`db/engine.py`** — Core database engine (CRUD, indexing, JOINs)
- **`db/table.py`** — Table class, row storage, constraint enforcement
- **`db/schema.py`** — Column class with type & constraint metadata
- **`db/storage.py`** — JSON-based persistence for tables & indexes
- **`repl.py`** — Interactive shell for SQL commands

---

## ⚡ Design Decisions

- **JSON persistence** — Easy to inspect and sufficient for small datasets
- **Dictionary indexes** — Fast lookups for PRIMARY/UNIQUE columns
- **REPL parser separate from engine** — Clean modular design
- **Human-readable errors** — Step 5 polish ensures no Python tracebacks
- **JOINs supported** — INNER JOIN between tables, with optional WHERE filters

---

## 📦 How to Run

### Clone the repo:
```bash
git clone git@github.com:cjkakai/pesapal-rdms.git
cd pesapal-rdms
```

### Run the REPL:
```bash
python repl.py
```

### Example session:
```
db> CREATE TABLE users (id INT PRIMARY KEY, name TEXT);
db> INSERT INTO users VALUES (1, 'Alice');
db> SELECT * FROM users;
{'id': 1, 'name': 'Alice'}
db> EXIT
```

---

## ✅ Notes / Limitations

- Supports only `INT` and `TEXT` columns
- Only `INNER JOIN` is implemented (no LEFT/RIGHT JOINs)
- `WHERE` clauses support only `=`, `>`, `<` operators
- No transactions or multi-user concurrency
- Designed for demonstration and small datasets

---

## 📚 Next Steps / Improvements

- Column selection in queries: `SELECT users.name, orders.total`
- `LEFT`/`RIGHT JOIN` support
- Enhanced query parsing and syntax validation
- Index-aware JOIN optimization
- ACID compliance / transaction support