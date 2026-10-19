# checks for notes/092-relationships-one-customer-many-orders.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
piles = {}
for oid, cid in con.execute("SELECT order_id, customer_id FROM orders ORDER BY 1").fetchall():
    piles.setdefault(cid, []).append(oid)
assert piles == {1: [101,103,106], 2: [102,107], 3: [104], 4: [105]}
assert [len(piles.get(c, [])) for c in (1,2,3,4,5)] == [3,2,1,1,0]
assert 3 + 2 + 1 + 1 + 0 == 7 == sum(len(v) for v in piles.values())
assert con.execute("SELECT count(*) FROM customers").fetchone()[0] == 5
print("092 ok")
