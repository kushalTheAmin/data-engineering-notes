# checks for notes/094-what-a-foreign-key-stops.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
import duckdb
con = shop()
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
assert con.execute("SELECT count(*) FROM customers WHERE customer_id = 9").fetchone()[0] == 0
try:
    con.execute("INSERT INTO orders VALUES (108, 9, TIMESTAMP '2026-04-10 10:00:00', 'new')")
    raise SystemExit("insert should fail")
except duckdb.ConstraintException as e:
    assert "does not exist in the referenced table" in str(e)
assert con.execute("SELECT order_id FROM orders WHERE customer_id = 3").fetchall() == [(104,)]
try:
    con.execute("DELETE FROM customers WHERE customer_id = 3")
    raise SystemExit("delete should fail")
except duckdb.ConstraintException as e:
    assert "still referenced" in str(e)
assert con.execute("SELECT count(*) FROM orders WHERE customer_id = 5").fetchone()[0] == 0
con.execute("DELETE FROM customers WHERE customer_id = 5")
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 4
sql = open(os.path.join(os.path.dirname(__file__), "..", "data", "shop.sql")).read()
assert "PRIMARY KEY (order_id, product_id)" in sql
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
# confirmed: ON DELETE CASCADE deletes the referencing rows when a referenced row is deleted, and order items inside an order are the docs example where it fits
print("094 ok")
