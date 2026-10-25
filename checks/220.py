# checks for notes/220-insert-adding-rows-and-matching-values-to-columns.md
import os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the ids used: Chirag 3, Disha 4, jalebi 3, kaju katli 4
assert q("SELECT customer_id, name FROM customers WHERE customer_id IN (3, 4) ORDER BY 1") == [(3, "Chirag"), (4, "Disha")]
assert q("SELECT product_id, name FROM products WHERE product_id IN (3, 4) ORDER BY 1") == [(3, "jalebi"), (4, "kaju katli")]
con.execute("CREATE TABLE wishlist (customer_id INTEGER, product_id INTEGER, added_on DATE)")
con.execute("INSERT INTO wishlist VALUES (1, 1, '2026-04-01'), (2, 3, '2026-04-02')")
con.execute("INSERT INTO wishlist (product_id, customer_id) VALUES (1, 5)")
con.execute("INSERT INTO wishlist VALUES (4, 3, '2026-04-03')")
d = datetime.date
assert q("SELECT * FROM wishlist ORDER BY customer_id") == [(1, 1, d(2026, 4, 1)), (2, 3, d(2026, 4, 2)), (4, 3, d(2026, 4, 3)), (5, 1, None)]
try:
    con.execute("INSERT INTO wishlist VALUES (5, 2)")
    assert False
except Exception as e:
    assert "3 columns" in str(e)
# source: https://www.postgresql.org/docs/current/sql-insert.html
#   confirmed (opened this run): with no column list the default is all columns in declared order, or the first N if only N values are supplied; columns not listed get their default or null; the standard disallows that case but Postgres permits it.
