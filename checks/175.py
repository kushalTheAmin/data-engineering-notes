# checks for notes/175-subquery-in-from.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
try:
    q("SELECT avg(count(*)) FROM orders GROUP BY customer_id")
    raise SystemExit("should have failed")
except Exception as e:
    assert "aggregate function calls cannot be nested" in str(e)
inner = "SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id"
assert q(inner + " ORDER BY customer_id") == [(1, 3), (2, 2), (3, 1), (4, 1)]
assert q("SELECT avg(orders) FROM (" + inner + ") AS per_customer") == [(1.75,)]
# python version: counts first, then sum over len
counts = [n for _, n in q(inner)]
assert sum(counts) / len(counts) == 1.75 and sum(counts) == 7 and len(counts) == 4
assert q("SELECT count(*) FROM orders") == [(7,)]
# esha has no orders, counting her would give 7 / 5
assert q("SELECT count(*) FROM customers") == [(5,)] and 7 / 5 == 1.4
assert q("SELECT count(*) FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)") == [(1,)]
# check yourself 1
assert q("SELECT avg(orders) FROM (" + inner + ") AS per_customer WHERE orders >= 2") == [(2.5,)] and (3 + 2) / 2 == 2.5
# check yourself 2
d = "SELECT customer_id, count(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY customer_id"
assert q(d + " ORDER BY customer_id") == [(1, 2), (2, 2), (4, 1)]
assert q("SELECT round(avg(orders), 2) FROM (" + d + ") AS per_customer") == [(1.67,)] and round(5 / 3, 2) == 1.67
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "Subqueries specifying a derived table must be enclosed in parentheses. They may be assigned a table alias name" and a subquery in FROM with grouping or aggregation cannot be reduced to a plain join
