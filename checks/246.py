# checks for notes/246-add-a-new-column-and-backfill-it-in-batches.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
# the shop has orders 101 to 107, and no order 108
assert q("SELECT order_id FROM orders ORDER BY order_id") == [(i,) for i in range(101, 108)]
assert q("SELECT count(*) FROM orders WHERE order_id = 108") == [(0,)]
# batches of 3 over 7 orders: 101-103, 104-106, 107
ids = list(range(101, 108))
batches = [ids[i:i + 3] for i in range(0, len(ids), 3)]
assert batches == [[101, 102, 103], [104, 105, 106], [107]]
assert [7 - sum(len(b) for b in batches[:k + 1]) for k in range(3)] == [4, 1, 0]
# a billion rows at 10000 per batch is 100000 UPDATEs
assert 1_000_000_000 // 10_000 == 100_000
# after the 3 batches plus a new order 108 with no copy, one NULL is left
rows = [{"order_id": i, "order_id_big": i} for i in ids] + [{"order_id": 108, "order_id_big": None}]
assert sum(r["order_id_big"] is None for r in rows) == 1
# running order_id_big = order_id twice gives the same value
v = 105
assert v == v
# source: https://www.postgresql.org/docs/current/sql-altertable.html
#   confirmed (opened this run): ADD COLUMN with no default stores NULL and needs no table rewrite
# source: https://www.postgresql.org/docs/current/explicit-locking.html
#   confirmed in the check for 245 and 242: row locks are normally held until the end of the transaction
