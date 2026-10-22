# checks for notes/148-conditional-aggregation-counting-several-things-in-one-pass.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT customer_id, count(*) AS total, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending FROM orders GROUP BY customer_id ORDER BY customer_id") == [(1, 3, 2, 1), (2, 2, 2, 0), (3, 1, 0, 0), (4, 1, 1, 0)]
# Asha: 3 orders, 2 delivered, 1 pending (note 147 counted only 2 after WHERE)
assert dict(q("SELECT customer_id, count(*) FROM orders WHERE status = 'delivered' GROUP BY customer_id"))[1] == 2
assert 3 not in dict(q("SELECT customer_id, count(*) FROM orders WHERE status = 'delivered' GROUP BY customer_id"))
assert q("SELECT count(CASE WHEN status = 'pending' THEN 1 ELSE 0 END), count(CASE WHEN status = 'pending' THEN 1 END) FROM orders") == [(7, 1)]
# check yourself
assert q("SELECT count(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE status = 'delivered'") == [(5,)]
assert q("SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 END) FROM orders WHERE customer_id IN (2, 3) GROUP BY customer_id ORDER BY customer_id") == [(2, 2), (3, None)]
assert q("SELECT status FROM orders WHERE customer_id = 3") == [("cancelled",)]
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed (sum with no non-null input gives null; asserted above for DuckDB): "except for count, these functions return a null value when no rows are selected. In particular, sum of no rows returns null, not zero", and coalesce can substitute zero
