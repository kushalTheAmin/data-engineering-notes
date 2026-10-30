# checks for notes/275-merge-sort-split-down-to-single-items-then-merge-back-up.md
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

def rounds(n):
    lists, r = n, 0
    while lists > 1:
        lists = (lists + 1) // 2
        r += 1
    return r

rows = con.execute("SELECT name, price FROM products ORDER BY product_id").fetchall()
assert [(n, float(p)) for n, p in rows] == [("dhokla", 6.0), ("khandvi", 7.5), ("jalebi", 5.0), ("kaju katli", 12.0), ("masala chai", 3.0), ("fafda", 4.5)]
assert len(rows) == 6
lists = [[float(p)] for n, p in rows]
history = [lists]
while len(lists) > 1:
    merged = [merge(lists[k], lists[k + 1]) for k in range(0, len(lists) - 1, 2)]
    if len(lists) % 2 == 1:
        merged.append(lists[-1])
    lists = merged
    history.append(lists)
# 3 rounds, 3 pairs then 2 lists then 1
assert len(history) - 1 == 3 and rounds(6) == 3
assert [len(h) for h in history] == [6, 3, 2, 1]
assert history[-1][0] == sorted(float(p) for n, p in rows)
# check yourself 1: 12 products -> 4 rounds, not 6
assert rounds(12) == 4
# check yourself 2: merging unsorted halves changes nothing
assert merge([6.0, 7.5, 5.0], [12.0, 3.0, 4.5]) == [6.0, 7.5, 5.0, 12.0, 3.0, 4.5]
# source: https://en.wikipedia.org/wiki/Timsort
# confirmed: Timsort is a hybrid, stable sorting algorithm, derived from merge sort and insertion sort, implemented for Python
# source: https://docs.python.org/3/howto/sorting.html
# confirmed: the Sorting HOWTO says the Timsort algorithm is used in Python
# source: https://en.wikipedia.org/wiki/Timsort
# confirmed: the algorithm finds subsequences of the data that are already ordered (runs)
