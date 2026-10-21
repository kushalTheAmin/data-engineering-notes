# checks for notes/137-aggregate-functions-many-rows-in-one-value-out.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT quantity FROM order_items")
assert len(rows) == 13
assert q("SELECT count(*), sum(quantity), max(quantity) FROM order_items") == [(13, 20, 3)]
assert (len(rows), sum(r[0] for r in rows), max(r[0] for r in rows)) == (13, 20, 3)
assert q("SELECT count(*), sum(quantity) FROM order_items WHERE order_id = 999") == [(0, None)]
assert q("SELECT count(*) FROM orders WHERE order_id = 999") == [(0,)]
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: "except for count, these functions return a null value when no rows are selected. In particular, sum of no rows returns null, not zero"
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: "PostgreSQL uses a client/server model"
