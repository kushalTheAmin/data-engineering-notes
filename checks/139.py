# checks for notes/139-count-distinct-counting-different-values.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
ids = [r[0] for r in q("SELECT customer_id FROM orders ORDER BY order_id")]
assert ids == [1, 2, 1, 3, 4, 1, 2]
seen = []
for c in ids:
    if c not in seen:
        seen.append(c)
assert (len(ids), len(seen)) == (7, 4)
assert ids.count(1) == 3 and ids.count(2) == 2
assert q("SELECT count(*), count(DISTINCT customer_id) FROM orders") == [(7, 4)]
assert q("SELECT count(*), count(city), count(DISTINCT city) FROM customers") == [(5, 4, 3)]
assert q("SELECT DISTINCT city FROM customers").count((None,)) == 1
# source: https://www.postgresql.org/docs/current/sql-expressions.html
# confirmed: "count(distinct f1) yields the number of distinct non-null values of f1"
