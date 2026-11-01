# checks for notes/292-covering-index-when-the-index-alone-has-the-answer.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
rows = q("SELECT customer_id, strftime(ordered_at, '%Y-%m-%d %H:%M:%S'), order_id, status FROM orders WHERE customer_id = 1 ORDER BY ordered_at")
assert [(a, b, c) for a, b, c, d in rows] == [
    (1, "2026-04-01 09:15:00", 101), (1, "2026-04-03 12:05:00", 103), (1, "2026-04-08 10:00:00", 106)]
assert {c: d for a, b, c, d in rows} == {101: "delivered", 103: "delivered", 106: "pending"}
# 3 entries for Asha, status needs one trip per entry, ordered_at needs none
assert len(rows) == 3
# source: https://www.postgresql.org/docs/16/indexes-index-only-scans.html
# confirmed: index-only scans answer from the index alone when the query references only columns stored in the index; the visibility map bit is checked and the heap is visited if not set; INCLUDE adds extra columns to build a covering index (opened this run)
