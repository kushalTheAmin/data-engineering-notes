# checks for notes/144-grouping-by-more-than-one-column.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id ORDER BY 1")[0] == (1, 3)
pairs = q("SELECT customer_id, status, count(*) FROM orders GROUP BY customer_id, status ORDER BY 1, 2")
assert pairs == [(1, "delivered", 2), (1, "pending", 1), (2, "delivered", 2), (3, "cancelled", 1), (4, "delivered", 1)]
assert len(pairs) == 5 and sum(n for _, _, n in pairs) == 7
# 4 customers with orders times 3 statuses (the customers table has 5 rows, one never ordered)
assert q("SELECT count(*) FROM customers") == [(5,)]
assert q("SELECT count(DISTINCT customer_id) FROM orders") == [(4,)]
assert q("SELECT count(DISTINCT status) FROM orders") == [(3,)]
assert 4 * 3 == 12
assert (2, "cancelled") not in [(c, s) for c, s, _ in pairs]
# column order does not change the groups
swapped = q("SELECT status, customer_id, count(*) FROM orders GROUP BY status, customer_id")
assert sorted((c, s, n) for s, c, n in swapped) == sorted(pairs)
# python shape: tuple keys
rows = q("SELECT customer_id, status FROM orders")
d = {}
for k in rows:
    d[k] = d.get(k, 0) + 1
assert d[(1, "delivered")] == 2
# check yourself 1
assert q("SELECT status, count(*) FROM orders GROUP BY status ORDER BY 1") == [("cancelled", 1), ("delivered", 5), ("pending", 1)]
assert [(c, n) for c, s, n in pairs if s == "delivered"] == [(1, 2), (2, 2), (4, 1)]
# check yourself 2
assert q("SELECT customer_id, status, count(*) FROM orders WHERE status <> 'pending' GROUP BY customer_id, status ORDER BY 1, 2") == [(1, "delivered", 2), (2, "delivered", 2), (3, "cancelled", 1), (4, "delivered", 1)]
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "WHERE filters individual rows before the application of GROUP BY, while HAVING filters group rows created by GROUP BY"
