# checks for notes/291-the-leftmost-prefix-rule-which-questions-a-composite-index-can-answer.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT customer_id, strftime(ordered_at, '%Y-%m-%d %H:%M:%S'), order_id FROM orders ORDER BY customer_id, ordered_at")
index = [tuple(r) for r in rows]
assert index == [
    (1, "2026-04-01 09:15:00", 101), (1, "2026-04-03 12:05:00", 103),
    (1, "2026-04-08 10:00:00", 106), (2, "2026-04-01 18:40:00", 102),
    (2, "2026-04-09 13:45:00", 107), (3, "2026-04-04 08:30:00", 104),
    (4, "2026-04-06 19:10:00", 105),
]
hits = lambda t: [i for i, e in enumerate(index) if t(e)]
assert hits(lambda e: e[0] == 1) == [0, 1, 2]
assert hits(lambda e: e[0] == 1 and e[1] >= "2026-04-03") == [1, 2]
assert hits(lambda e: e[1] >= "2026-04-06") == [2, 4, 6]
oi = q("SELECT product_id, order_id FROM order_items ORDER BY product_id, order_id")
assert len(oi) == 13
assert [i for i, (p, o) in enumerate(oi) if o == 105] == [6, 9, 12]
assert q("SELECT order_id, product_id FROM order_items WHERE order_id = 105 AND product_id >= 4 ORDER BY product_id") == [(105, 4), (105, 5)]
assert q("SELECT product_id FROM order_items WHERE order_id = 105 ORDER BY product_id") == [(3,), (4,), (5,)]
# source: https://www.postgresql.org/docs/16/indexes-multicolumn.html
# confirmed: leading column constraints limit the scanned portion; a condition on later columns alone means the entire index is scanned and the planner would usually prefer a sequential scan (opened this run)
# source: https://www.postgresql.org/docs/18/indexes-multicolumn.html
# confirmed: version 18 docs describe skip scan, generally taken only when there are few distinct values in the skipped column (opened this run)
# audit: product_id has 5 distinct values in order_items, the few-distinct-values case where a version 18 skip scan could avoid reading all 13 entries, so check yourself 1 says without a skip scan
assert len(q("SELECT DISTINCT product_id FROM order_items")) == 5
