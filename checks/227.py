# checks for notes/227-transactions-all-or-nothing.md
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
con.execute("CREATE TABLE my_orders AS SELECT * FROM orders")
con.execute("CREATE TABLE my_items (order_id INTEGER, product_id INTEGER REFERENCES products (product_id), quantity INTEGER)")
con.execute("INSERT INTO my_items SELECT * FROM order_items")
con.execute("INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending')")
assert fails("INSERT INTO my_items VALUES (108, 99, 1)")
assert q("SELECT count(*) FROM my_orders WHERE order_id = 108") == [(1,)]
assert q("SELECT count(*) FROM my_items WHERE order_id = 108") == [(0,)]
assert q("SELECT name FROM customers WHERE customer_id = 4") == [("Disha",)]
assert q("SELECT name FROM products WHERE product_id = 1") == [("dhokla",)]
assert q("SELECT count(*) FROM products WHERE product_id = 99") == [(0,)]
con.execute("INSERT INTO my_orders VALUES (109, 4, TIMESTAMP '2026-04-10 12:00:00', 'pending')")
con.execute("INSERT INTO my_items VALUES (109, 1, 1)")
assert fails("INSERT INTO my_items VALUES (109, 99, 1)")
assert q("SELECT count(*) FROM my_items WHERE order_id = 109") == [(1,)]
assert q("SELECT product_id FROM my_items WHERE order_id = 102 ORDER BY product_id") == [(3,), (4,)]
assert q("SELECT count(*) FROM products WHERE product_id IN (6, 7)") == [(1,)]
assert fails("UPDATE my_items SET product_id = product_id + 3 WHERE order_id = 102")
assert q("SELECT product_id FROM my_items WHERE order_id = 102 ORDER BY product_id") == [(3,), (4,)]
# source: https://www.postgresql.org/docs/current/tutorial-transactions.html
# confirmed: a transaction bundles multiple steps into a single all-or-nothing operation; the page's example is a bank payment from Alice's account to Bob's; PostgreSQL treats every SQL statement as executed within a transaction
