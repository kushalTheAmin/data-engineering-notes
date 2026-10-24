# checks for notes/198-date-spines-a-left-join-that-keeps-the-empty-days.md
import os, sys
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
d = lambda n: date(2026, 4, n)
SPINE = "generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS s(d)"
JOIN = "LEFT JOIN orders o ON CAST(o.ordered_at AS DATE) = CAST(s.d AS DATE)"
# grouping orders by day alone gives 6 rows, the spine gives 9
assert q("SELECT count(DISTINCT CAST(ordered_at AS DATE)) FROM orders") == [(6,)]
rows = q(f"SELECT CAST(s.d AS DATE) AS day, count(o.order_id) AS orders FROM {SPINE} {JOIN} GROUP BY day ORDER BY day")
assert len(rows) == 9 and [r[1] for r in rows] == [2, 0, 1, 1, 0, 1, 0, 1, 1]
assert [r[0] for r in rows if r[1] == 0] == [d(2), d(5), d(7)]
# python version: dict with a default
placed = {}
for (ts,) in q("SELECT ordered_at FROM orders"):
    placed[ts.date()] = placed.get(ts.date(), 0) + 1
assert [placed.get(d(n), 0) for n in range(1, 10)] == [2, 0, 1, 1, 0, 1, 0, 1, 1]
# average per day: 7 over 6 versus 7 over 9
assert sum(placed.values()) == 7 and len(placed) == 6
assert round(7 / 6, 2) == 1.17 and round(7 / 9, 2) == 0.78
# answer 1: count(*) gives 1 for april 5
assert q(f"SELECT count(*) AS orders FROM generate_series(DATE '2026-04-05', DATE '2026-04-05', INTERVAL 1 DAY) AS s(d) {JOIN}") == [(1,)]
# answer 2: WHERE on status leaves 4 days, april 4 is cancelled and april 8 pending
rows = q(f"SELECT CAST(s.d AS DATE) AS day, count(o.order_id) AS orders FROM {SPINE} {JOIN} WHERE o.status = 'delivered' GROUP BY day ORDER BY day")
assert rows == [(d(1), 2), (d(3), 1), (d(6), 1), (d(9), 1)]
assert q("SELECT order_id, status FROM orders WHERE order_id IN (104, 106) ORDER BY order_id") == [(104, 'cancelled'), (106, 'pending')]
# the fix: test in ON keeps all 9 days
assert q(f"SELECT count(*) FROM (SELECT CAST(s.d AS DATE) AS day FROM {SPINE} LEFT JOIN orders o ON CAST(o.ordered_at AS DATE) = CAST(s.d AS DATE) AND o.status = 'delivered' GROUP BY day)") == [(9,)]
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: "the joined table always has at least one row for each row in T1" (unmatched left rows get null values in the right columns)
