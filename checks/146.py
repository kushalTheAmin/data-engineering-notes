# checks for notes/146-having-filtering-whole-groups.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM orders") == [(7,)]
assert q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id HAVING count(*) >= 2 ORDER BY 1") == [(1, 3), (2, 2)]
counts = dict(q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id"))
assert counts == {1: 3, 2: 2, 3: 1, 4: 1}
kept = {c: n for c, n in counts.items() if n >= 2}
assert kept == {1: 3, 2: 2}
# customers 3 and 4 have one order each
assert counts[3] == 1 and counts[4] == 1
# max in HAVING, not selected
assert q("SELECT customer_id FROM orders GROUP BY customer_id HAVING max(ordered_at) > TIMESTAMP '2026-04-05 00:00:00' ORDER BY 1") == [(1,), (2,), (4,)]
# customer 3's only order is april 4, customer 4's is april 6
assert str(q("SELECT ordered_at FROM orders WHERE customer_id = 3")[0][0]) == "2026-04-04 08:30:00"
assert str(q("SELECT ordered_at FROM orders WHERE customer_id = 4")[0][0]) == "2026-04-06 19:10:00"
# check yourself 1
assert q("SELECT customer_id, count(*) FROM orders GROUP BY customer_id HAVING count(*) > 5") == []
assert max(counts.values()) == 3
# slice in prose: latest order per customer
assert [(c, str(t)[:10]) for c, t in q("SELECT customer_id, max(ordered_at) FROM orders GROUP BY customer_id ORDER BY 1")] == [(1, "2026-04-08"), (2, "2026-04-09"), (3, "2026-04-04"), (4, "2026-04-06")]
# check yourself 2
assert q("SELECT customer_id FROM orders GROUP BY customer_id HAVING max(ordered_at) > TIMESTAMP '2026-04-08 12:00:00' ORDER BY 1") == [(2,)]
assert str(q("SELECT max(ordered_at) FROM orders WHERE customer_id = 1")[0][0]) == "2026-04-08 10:00:00"
# source: https://www.postgresql.org/docs/current/sql-select.html
# confirmed: "HAVING eliminates group rows that do not satisfy the condition"; "WHERE filters individual rows before the application of GROUP BY, while HAVING filters group rows created by GROUP BY"
# TIMESTAMP is a day plus a clock time
assert q("SELECT typeof(ordered_at) FROM orders LIMIT 1") == [("TIMESTAMP",)]
assert str(q("SELECT TIMESTAMP '2026-04-05 00:00:00'")[0][0]) == "2026-04-05 00:00:00"
# source: https://duckdb.org/docs/2.0/sql/data_types/timestamp.html
# confirmed: "Timestamps represent points in time. As such, they combine DATE and TIME information."
