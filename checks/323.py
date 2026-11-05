# checks for notes/323-latency-and-bandwidth-slow-vs-narrow.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
latency = 0.05
order = 200
def seconds(r, s, bw): return r * (latency + s / bw)
rows = [(100, order), (1, 100 * order), (1, 100_000_000)]
assert [round(seconds(r, s, 1_000_000), 3) for r, s in rows] == [5.02, 0.07, 100.05]
assert [round(seconds(r, s, 10_000_000), 3) for r, s in rows] == [5.002, 0.052, 10.05]
assert round(5.02 / 0.07) == 72  # about 72 times
assert 100 * order / 1_000_000 == 0.02  # data time of the first row
assert round(5.02 - 5.002, 3) == 0.018
assert round(seconds(100, order, 100_000_000), 4) == 5.0002
assert round(seconds(1, 100_000_000, 100_000_000), 2) == 1.05
assert [r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id = 1 ORDER BY order_id").fetchall()] == [101, 103, 106]
assert round(3 * 0.05, 2) == 0.15
total = 10000 * order / 1_000_000
assert total == 2.0
assert round(100 * 0.05 + total, 2) == 7.0 and round(10 * 0.05 + total, 2) == 2.5
assert round(7.0 / 2.5, 1) == 2.8
# source: https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
#   confirmed (opened this run): per_page sets results per page, for most endpoints the max is 100, a larger value is silently lowered to the max
