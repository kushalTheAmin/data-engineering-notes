# checks for notes/147-where-vs-having-before-grouping-or-after.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT order_id FROM orders WHERE status = 'delivered' ORDER BY 1") == [(101,), (102,), (103,), (105,), (107,)]
sizes = dict(q("SELECT customer_id, count(*) FROM orders WHERE status = 'delivered' GROUP BY customer_id"))
assert sizes == {1: 2, 2: 2, 4: 1}
assert len(sizes) == 3
assert q("SELECT customer_id, count(*) AS n FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING count(*) >= 2 ORDER BY 1") == [(1, 2), (2, 2)]
# without the WHERE, Asha counts 3 (note 146)
assert dict(q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id"))[1] == 3
# customer 3 has one order and it is cancelled, so no group
assert q("SELECT status FROM orders WHERE customer_id = 3") == [("cancelled",)]
assert 3 not in sizes
# Asha has a pending order, so she has two different statuses
assert sorted(s for (s,) in q("SELECT DISTINCT status FROM orders WHERE customer_id = 1")) == ["delivered", "pending"]
# failing queries
for bad in ["SELECT customer_id, count(*) AS n FROM orders WHERE count(*) >= 2 GROUP BY customer_id",
            "SELECT customer_id FROM orders GROUP BY customer_id HAVING status = 'delivered'"]:
    failed = False
    try:
        q(bad)
    except Exception:
        failed = True
    assert failed
# check yourself 2
assert q("SELECT customer_id, count(*) AS n FROM orders WHERE status = 'delivered' GROUP BY customer_id HAVING count(*) >= 3") == []
# source: https://www.postgresql.org/docs/current/tutorial-agg.html
# confirmed: "WHERE selects input rows before groups and aggregates are computed", "the WHERE clause must not contain aggregate functions", and WHERE is "more efficient than adding the restriction to HAVING, because we avoid doing the grouping and aggregate calculations for all rows that fail the WHERE check"
# source: https://www.postgresql.org/docs/current/tutorial-arch.html
# confirmed: PostgreSQL uses a client/server model
# a test on a grouped column runs in HAVING too
assert q("SELECT customer_id FROM orders GROUP BY customer_id HAVING customer_id = 1") == [(1,)]
