# checks for notes/223-delete-removing-rows-and-what-still-points-at-them.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# order 104 is cancelled and is pointed at by one order_items row and one order_fees row
assert q("SELECT status FROM orders WHERE order_id = 104") == [("cancelled",)]
try:
    con.execute("DELETE FROM orders WHERE order_id = 104")
    raise SystemExit("delete should have failed")
except Exception as e:
    assert "foreign key" in str(e)
assert q("""SELECT 'order_items' AS tbl, count(*) AS rows_for_104 FROM order_items WHERE order_id = 104
UNION ALL SELECT 'order_fees', count(*) FROM order_fees WHERE order_id = 104
UNION ALL SELECT 'order_ratings', count(*) FROM order_ratings WHERE order_id = 104""") == [("order_items", 1), ("order_fees", 1), ("order_ratings", 0)]
from decimal import Decimal
assert q("SELECT fee FROM order_fees WHERE order_id = 104") == [(Decimal("0.00"),)]
# question 1: stars < 4 is true only for the 3, NULL rows are unknown and stay
assert q("SELECT stars FROM order_ratings ORDER BY order_id") == [(5,), (4,), (None,), (3,), (None,)]
assert q("DELETE FROM order_ratings WHERE stars < 4") == [(1,)]
assert q("SELECT count(*) FROM order_ratings") == [(4,)]
# question 2: fafda (6) is in no order, dhokla (1) is in orders 101 and 107 once 104's item is gone
con.execute("DELETE FROM order_items WHERE order_id = 104")
assert q("SELECT count(*) FROM order_items WHERE product_id = 6") == [(0,)]
assert q("SELECT order_id FROM order_items WHERE product_id = 1 ORDER BY order_id") == [(101,), (107,)]
assert q("DELETE FROM products WHERE name = 'fafda'") == [(1,)]
assert q("SELECT count(*) FROM products") == [(5,)]
try:
    con.execute("DELETE FROM products WHERE name = 'dhokla'")
    raise SystemExit("delete should have failed")
except Exception as e:
    assert "foreign key" in str(e)
# a DELETE with no WHERE removes every row and keeps the table
assert q("DELETE FROM order_ratings") == [(4,)]
assert q("SELECT count(*) FROM order_ratings") == [(0,)]
# source: https://www.postgresql.org/docs/current/sql-delete.html
