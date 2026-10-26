# checks for notes/230-acid-consistency-the-rules-still-hold-after-every-change.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
def fails(s):
    try:
        con.execute(s)
    except Exception:
        return True
    return False
con.execute("CREATE TABLE my_products (product_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0))")
con.execute("INSERT INTO my_products SELECT product_id, name, price FROM products")
con.execute("BEGIN")
con.execute("UPDATE my_products SET price = 7.00 WHERE name = 'dhokla'")
assert fails("UPDATE my_products SET price = -1 WHERE name = 'kaju katli'")
con.execute("COMMIT")
r = q("SELECT name, price FROM my_products WHERE name IN ('dhokla', 'kaju katli') ORDER BY name")
assert [(a, float(b)) for a, b in r] == [("dhokla", 6.0), ("kaju katli", 12.0)]
# an order with no items passes every declared rule
con.execute("CREATE TABLE my_orders AS SELECT * FROM orders")
con.execute("CREATE TABLE my_items AS SELECT * FROM order_items")
con.execute("INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending')")
assert q("SELECT o.order_id FROM my_orders o LEFT JOIN my_items i ON i.order_id = o.order_id WHERE i.order_id IS NULL") == [(108,)]
# source: https://www.postgresql.org/docs/current/ddl-constraints.html
#   confirmed (opened this run): "PostgreSQL does not support CHECK constraints that reference table data other than the new or updated row being checked"
