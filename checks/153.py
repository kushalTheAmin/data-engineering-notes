# checks for notes/153-the-full-run-order-with-group-by-and-having.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT count(*) FROM orders WHERE status <> 'cancelled'") == [(6,)]
assert q("SELECT order_id FROM orders WHERE status = 'cancelled'") == [(104,)]
sizes = dict(q("SELECT customer_id, count(*) FROM orders WHERE status <> 'cancelled' GROUP BY customer_id"))
assert sizes == {1: 3, 2: 2, 4: 1}
assert len(sizes) == 3
assert len({c: n for c, n in sizes.items() if n >= 2}) == 2
assert q("SELECT customer_id, count(*) AS n FROM orders WHERE status <> 'cancelled' GROUP BY customer_id HAVING count(*) >= 2 ORDER BY n DESC") == [(1, 3), (2, 2)]
assert q("SELECT customer_id, count(*) AS n FROM orders WHERE status <> 'cancelled' GROUP BY customer_id HAVING count(*) >= 2 ORDER BY n DESC LIMIT 1") == [(1, 3)]
# check yourself 1
assert q("SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id HAVING count(*) >= 2 ORDER BY n, customer_id LIMIT 1") == [(2, 2)]
assert q("SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id ORDER BY n, customer_id LIMIT 1") == [(3, 1)]
# check yourself 2
try:
    q("SELECT customer_id FROM orders GROUP BY customer_id HAVING status <> 'cancelled'")
    raise SystemExit("should fail")
except Exception as e:
    assert not isinstance(e, SystemExit)
# DuckDB accepts an AS name in HAVING
assert q("SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id HAVING n >= 2 ORDER BY 1") == [(1, 3), (2, 2)]
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "An output column's name can be used to refer to the column's value in ORDER BY and GROUP BY clauses, but not in the WHERE or HAVING clauses"
# and: "WHERE filters individual rows before the application of GROUP BY, while HAVING filters group rows created by GROUP BY"
# a LIMIT before HAVING would keep only customer 3 (n = 1), which HAVING then drops: no rows
assert q("SELECT customer_id, count(*) AS n FROM (SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id ORDER BY n, customer_id LIMIT 1) GROUP BY customer_id HAVING count(*) >= 2") == []
assert q("SELECT customer_id, n FROM (SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id ORDER BY n, customer_id LIMIT 1) WHERE n >= 2") == []
