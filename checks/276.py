# checks for notes/276-why-sorting-costs-more-than-one-pass-over-the-data.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

def sort_rounds(items):
    lists, placed = [[x] for x in items], []
    while len(lists) > 1:
        merged, p = [], 0
        for k in range(0, len(lists) - 1, 2):
            merged.append(merge(lists[k], lists[k + 1]))
            p += len(merged[-1])
        if len(lists) % 2 == 1:
            merged.append(lists[-1])
        lists = merged
        placed.append((p, len(merged)))
    return placed

prices = [float(p) for (p,) in con.execute("SELECT price FROM products ORDER BY product_id").fetchall()]
assert len(prices) == 6
placed = sort_rounds(prices)
# table 1: 3 rounds, lists after 3, 2, 1, placed 6, 4, 6, total 16 vs one pass of 6, at most 3 x 6 = 18
assert [p for p, _ in placed] == [6, 4, 6]
assert [l for _, l in placed] == [3, 2, 1]
assert sum(p for p, _ in placed) == 16 and len(placed) * len(prices) == 18

# table 2
rows = {}
for n in [7, 70, 700, 7000]:
    r = len(sort_rounds(list(range(n))))
    actual = sum(p for p, _ in sort_rounds(list(range(n))))
    assert actual <= r * n
    rows[n] = (r, r * n, n * n)
assert rows[7] == (3, 21, 49)
assert rows[70] == (7, 490, 4900)
assert rows[700] == (10, 7000, 490000)
assert rows[7000] == (13, 91000, 49000000)
# about 13 times the steps for 10 times the orders, nowhere near 100
assert round(91000 / 7000) == 13 and 91000 / 7000 < 100
# a sort of 12 items needs 4 rounds, doubling adds one round
assert len(sort_rounds(list(range(6)))) == 3 and len(sort_rounds(list(range(12)))) == 4
# source: https://www.postgresql.org/docs/current/indexes-ordering.html
# confirmed: an index may deliver rows in sorted order so ORDER BY is honored without a separate sorting step; of the index types supported, only B-tree can produce sorted output
