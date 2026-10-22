# checks for notes/152-rollup-subtotals-and-grand-totals.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
r = q("SELECT customer_id, status, count(*) FROM orders GROUP BY ROLLUP (customer_id, status) ORDER BY customer_id NULLS LAST, status NULLS LAST")
assert len(r) == 10 == 5 + 4 + 1
assert r[2] == (1, None, 3) and r[-1] == (None, None, 7)
assert 2 + 1 == 3 and q("SELECT count(*) FROM orders")[0][0] == 7
# 5 pairs, 4 customers with orders, 1 grand total
assert q("SELECT count(*) FROM (SELECT 1 FROM orders GROUP BY customer_id, status)")[0][0] == 5
assert q("SELECT count(DISTINCT customer_id) FROM orders")[0][0] == 4
assert q("SELECT customer_id, count(*), grouping(customer_id) FROM orders GROUP BY ROLLUP (customer_id) ORDER BY customer_id NULLS LAST") == [(1, 3, 0), (2, 2, 0), (3, 1, 0), (4, 1, 0), (None, 7, 1)]
# swapping the columns gives subtotals per status instead
s = q("SELECT status, customer_id, count(*) FROM orders GROUP BY ROLLUP (status, customer_id) ORDER BY status NULLS LAST, customer_id NULLS LAST")
assert ('delivered', None, 5) in s
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: ROLLUP (e1, e2, e3, ...) represents the list and all prefixes of the list including the empty list; "total salary by department, division, and company-wide total"
# source: https://www.postgresql.org/docs/current/functions-aggregate.html
# confirmed: GROUPING returns a bit mask indicating which GROUP BY expressions are not included in the current grouping set
# the python-loop claim: 3 passes (both columns, customer alone, nothing)
assert len({(r[0], r[1]) for r in r if r[0] is not None and r[1] is not None}) == 5
assert len([x for x in r if x[0] is not None and x[1] is None]) == 4 and len([x for x in r if x[0] is None]) == 1
# swapped order: delivered subtotal is 5
assert ('delivered', None, 5) in s
assert q("SELECT name FROM customers WHERE customer_id = 1") == [("Asha",)]
