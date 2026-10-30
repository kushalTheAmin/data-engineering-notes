# checks for notes/271-curving-up-when-10-times-the-data-means-100-times-the-steps.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def look_at_every_pair(order_ids):
    steps = 0
    for i, a in enumerate(order_ids):
        for j, b in enumerate(order_ids):
            steps += 1
            if i != j and a == b:
                return steps
    return steps

# the shop has orders 101 to 107
assert [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()] == list(range(101, 108))
prev = None
for n in [7, 70, 700]:
    s = look_at_every_pair(list(range(101, 101 + n)))
    assert s == n * n
    if prev: assert s == prev * 100   # 10 times the orders, 100 times the steps
    prev = s
assert (49, 4900, 490000) == (7 * 7, 70 * 70, 700 * 700)
# a smarter version checking each pair once does about half, still near 100 times per 10 times
half = lambda n: n * (n - 1) // 2
assert half(7) == 21 and half(70) == 2415 and 100 * 0.9 < half(70) / half(7) < 100 * 1.3
# question 1
assert 4900 * 100 * 100 == 49000000 == 7000 * 7000 and 4900 * 100 == 490000
# question 2: seen list, checks add up to 0+1+...+6999
steps = 0
seen = []
for oid in range(101, 101 + 7000):
    for old in seen:
        steps += 1
    seen.append(oid)
assert steps == sum(range(7000)) == 24496500
# source: https://www.postgresql.org/docs/current/planner-optimizer.html
# confirmed: nested loop join "The right relation is scanned once for every row found in the left relation. This strategy is easy to implement but can be very time consuming."
