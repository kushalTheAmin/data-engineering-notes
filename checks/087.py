# checks for notes/087-primary-key.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
def refused(q):
    try:
        con.execute(q)
    except duckdb.ConstraintException:
        return True
    return False
assert refused("INSERT INTO customers VALUES (3, 'Chirag', 'Edison', DATE '2026-06-01')")
assert con.execute("SELECT customer_id, name, city FROM customers WHERE customer_id = 3").fetchall() == [(3, "Chirag", "Jersey City")]
assert con.execute("SELECT count(*) FROM customers WHERE name = 'Chirag'").fetchone()[0] == 1
assert con.execute("SELECT max(customer_id) FROM customers").fetchone()[0] == 5  # so the next new id is 6
# q1
assert refused("INSERT INTO orders VALUES (101, 2, TIMESTAMP '2026-05-01 10:00:00', 'pending')")
# q2
assert refused("INSERT INTO customers VALUES (NULL, 'Gita', 'Edison', DATE '2026-06-01')")
# q3
assert con.execute("SELECT customer_id, name FROM customers WHERE city = 'Jersey City' ORDER BY 1").fetchall() == [(1, "Asha"), (3, "Chirag")]
# UNIQUE alone allows many NULLs in DuckDB
con.execute("CREATE TABLE u (id INTEGER UNIQUE)")
con.execute("INSERT INTO u VALUES (NULL), (NULL)")
assert con.execute("SELECT count(*) FROM u").fetchone()[0] == 2
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
# confirmed: a primary key requires that the values be both unique and not null
# confirmed: by default, two null values are not considered equal in a unique comparison
# source: https://www.sqlite.org/lang_createtable.html
# confirmed: SQLite allows NULL values in most PRIMARY KEY columns (not INTEGER PRIMARY KEY, WITHOUT ROWID or STRICT tables)
print("087 ok")
