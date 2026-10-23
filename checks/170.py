# checks for notes/170-joining-on-a-range-matching-a-date-to-a-period.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
assert q("SELECT count(*) FROM promo_periods") == [(2,)]
bad = q("SELECT o.order_id FROM orders o JOIN promo_periods p ON o.ordered_at BETWEEN p.starts_on AND p.ends_on ORDER BY 1")
assert bad == [(101,), (102,), (105,)]
# order 103 is 12:05 on 2026-04-03, the last day of launch week, and a date end compares as midnight
assert q("SELECT ordered_at > CAST(DATE '2026-04-03' AS TIMESTAMP) FROM orders WHERE order_id = 103") == [(True,)]
assert q("SELECT strftime(ordered_at, '%Y-%m-%d %H:%M') FROM orders WHERE order_id = 103") == [("2026-04-03 12:05",)]
good = q("SELECT o.order_id, p.promo FROM orders o LEFT JOIN promo_periods p ON CAST(o.ordered_at AS DATE) BETWEEN p.starts_on AND p.ends_on ORDER BY 1")
assert len(good) == 7 == q("SELECT count(*) FROM orders")[0][0]
assert [r[0] for r in good if r[1] is None] == [104, 106, 107]
# order 104 is on april 4, between the two promos
assert q("SELECT CAST(ordered_at AS DATE) FROM orders WHERE order_id = 104")[0][0].isoformat() == "2026-04-04"
# source: https://www.postgresql.org/docs/current/queries-table-expressions.html
# confirmed: the ON clause takes any boolean expression, the same kind as used in WHERE
