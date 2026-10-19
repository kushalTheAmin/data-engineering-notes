# checks for notes/088-natural-keys-vs-made-up-ids.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
# asha is customer 1 with orders 101, 103, 106
assert [r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY 1").fetchall()] == [101, 103, 106]
# q1: product 4 has 2 order items, before and after a rename
assert con.execute("SELECT count(*) FROM order_items WHERE product_id = 4").fetchone()[0] == 2
con.execute("UPDATE products SET name = 'kaju katli (large)' WHERE product_id = 4")
assert con.execute("SELECT count(*) FROM order_items WHERE product_id = 4").fetchone()[0] == 2
# q2: a reused key value is refused even for a different person
con.execute("CREATE TABLE phones (phone VARCHAR PRIMARY KEY, name VARCHAR)")
con.execute("INSERT INTO phones VALUES ('555-0101', 'Bhavin')")
try:
    con.execute("INSERT INTO phones VALUES ('555-0101', 'Gita')")
    raise SystemExit("should have been refused")
except duckdb.ConstraintException:
    pass
# q3: id key accepts the same email twice, UNIQUE refuses it; new ids would be 6 and 7
assert con.execute("SELECT max(customer_id) FROM customers").fetchone()[0] == 5
con.execute("CREATE TABLE c (id INTEGER PRIMARY KEY, email VARCHAR)")
con.execute("INSERT INTO c VALUES (6, 'g@example.com'), (7, 'g@example.com')")
con.execute("CREATE TABLE c2 (id INTEGER PRIMARY KEY, email VARCHAR UNIQUE)")
con.execute("INSERT INTO c2 VALUES (6, 'g@example.com')")
try:
    con.execute("INSERT INTO c2 VALUES (7, 'g@example.com')")
    raise SystemExit("should have been refused")
except duckdb.ConstraintException:
    pass
con.execute("INSERT INTO c2 VALUES (8, 'h@example.com')")
assert con.execute("SELECT count(*) FROM c2").fetchone()[0] == 2
# source: https://www.postgresql.org/docs/current/ddl-identity-columns.html
# confirmed: "An identity column is a special column that is generated automatically from an implicit sequence. It can be used to generate key values."
print("088 ok")
