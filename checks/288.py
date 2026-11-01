# checks for notes/288-one-lookup-traced-through-a-b-tree.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
per_page = 136
signposts = [467, 833]
leaves = [list(range(101, 467)), list(range(467, 833)), list(range(833, 1101))]
assert [len(l) for l in leaves] == [366, 366, 268]
want = 500
child = sum(1 for s in signposts if want >= s)
assert child == 1 and 467 <= 500 < 833
leaf = leaves[child]
lo, hi, looks = 0, len(leaf) - 1, 0
while lo <= hi:
    mid = (lo + hi) // 2
    looks += 1
    if leaf[mid] == want:
        break
    if leaf[mid] < want:
        lo = mid + 1
    else:
        hi = mid - 1
assert looks == 8
assert ((want - 101) // per_page, (want - 101) % per_page + 1) == (2, 128)
# 3 reads = root + leaf + table page, the shared hit=3 of note 286
assert 1 + 1 + 1 == 3
# a signpost value belongs to the side above: 467 goes to the middle leaf
assert sum(1 for s in signposts if 467 >= s) == 1
# check yourself 1: toy leaves 101-103, 104-106, 107
assert q("SELECT order_id FROM orders WHERE order_id BETWEEN 103 AND 105 ORDER BY order_id") == [(103,), (104,), (105,)]
toy = [[101, 102, 103], [104, 105, 106], [107]]
assert [i for i, l in enumerate(toy) if any(o in l for o in (103, 104, 105))] == [0, 1]
# check yourself 2
assert 300 ** 2 == 90000 and 300 ** 3 == 27000000
assert 300 ** 2 < 20_000_000 <= 300 ** 3 and 3 + 1 == 4
# source: https://raw.githubusercontent.com/postgres/postgres/REL_16_STABLE/src/backend/access/nbtree/nbtsearch.c
#   confirmed: _bt_binsrch does a binary search for a key on a particular page (opened this run)
