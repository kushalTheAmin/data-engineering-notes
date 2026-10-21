# checks for notes/145-the-group-by-rule-every-column-is-grouped-or-aggregated.md
import os, sys
from decimal import Decimal
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
try:
    q("SELECT customer_id, status, count(*) AS n FROM orders GROUP BY customer_id")
    raise SystemExit("should have failed")
except Exception as e:
    assert "must appear in the GROUP BY clause" in str(e)
assert q("SELECT status FROM orders WHERE customer_id = 1 ORDER BY order_id") == [("delivered",), ("delivered",), ("pending",)]
orders = q("SELECT customer_id, status FROM orders ORDER BY order_id")
groups = {}
for customer_id, status in orders:
    groups.setdefault(customer_id, []).append(status)
assert groups[1] == ["delivered", "delivered", "pending"]
assert len(set(groups[1])) == 2 and len(groups[1]) == 3
r = q("SELECT customer_id, count(*), max(ordered_at) FROM orders GROUP BY customer_id ORDER BY 1")
assert [(c, n, str(t)) for c, n, t in r] == [(1, 3, "2026-04-08 10:00:00"), (2, 2, "2026-04-09 13:45:00"), (3, 1, "2026-04-04 08:30:00"), (4, 1, "2026-04-06 19:10:00")]
# check yourself 1
r = q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id, status ORDER BY customer_id, status")
assert r == [(1, 2), (1, 1), (2, 2), (3, 1), (4, 1)] and len(r) == 5
# check yourself 2
r = q("SELECT category, name, min(price) FROM products GROUP BY category, name ORDER BY category, name")
assert len(r) == 6 and q("SELECT count(DISTINCT name) FROM products") == [(6,)]
assert q("SELECT count(DISTINCT category) FROM products") == [(3,)]
assert r[0] == ("drink", "masala chai", Decimal("3.00"))
# source: https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html
# confirmed: ONLY_FULL_GROUP_BY is enabled by default; when disabled "the server is free to choose any value from each group" and the values are nondeterministic
# source: https://dev.mysql.com/doc/refman/8.4/en/what-is-mysql.html
# confirmed: "The MySQL Database Software is a client/server system"
