# checks for notes/274-merging-two-sorted-lists-into-one.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def merge(left, right):
    out, i, j, cmps = [], 0, 0, 0
    while i < len(left) and j < len(right):
        cmps += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:], cmps

price = dict(con.execute("SELECT name, price FROM products").fetchall())
assert price["fafda"] == 4.5 and price["dhokla"] == 6 and price["khandvi"] == 7.5
assert price["masala chai"] == 3 and price["jalebi"] == 5 and price["kaju katli"] == 12
left = ["fafda", "dhokla", "khandvi"]
right = ["masala chai", "jalebi", "kaju katli"]
assert [float(price[n]) for n in left] == sorted(float(price[n]) for n in left)
assert [float(price[n]) for n in right] == sorted(float(price[n]) for n in right)
out, cmps = merge([float(price[n]) for n in left], [float(price[n]) for n in right])
# 6 items, 5 comparisons, result sorted
assert len(out) == 6 and cmps == 5 and out == sorted(out)
assert len(left) + len(right) == 6
# check yourself 1: 2 comparisons
assert merge([4.5, 6.0], [7.5, 12.0]) == ([4.5, 6.0, 7.5, 12.0], 2)
assert 4 - 1 == 3
# check yourself 2
assert merge([6.0, 4.5], [3.0, 5.0])[0] == [3.0, 5.0, 6.0, 4.5]
# source: https://www.postgresql.org/docs/current/planner-optimizer.html
# confirmed: merge join sorts each relation on the join attributes, then scans the two in parallel, each only once
