# checks for notes/273-binary-search-finding-one-item-in-sorted-data-by-halving.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()

def find(order_ids, wanted):
    steps = 0
    for oid in order_ids:
        steps += 1
        if oid == wanted:
            return steps
    return steps

def halve_looks(ids, wanted):
    lo, hi, looks = 0, len(ids) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        looks += 1
        if ids[mid] == wanted:
            return looks
        if ids[mid] < wanted:
            lo = mid + 1
        else:
            hi = mid - 1
    return looks

# the shop has orders 101 to 107
assert [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()] == list(range(101, 108))
ids = list(range(101, 108))
# the trace: middle 104, then 106, then 107, three looks, 7 then 3 then 1 left
assert ids[(0 + 6) // 2] == 104
assert ids[4:][(0 + 2) // 2] == 106
assert halve_looks(ids, 107) == 3
assert ids[4:] == [105, 106, 107] and ids[6:] == [107]
assert len(ids) == 7 and len(ids[4:]) == 3 and len(ids[6:]) == 1
# the table: hunt vs halving, last id and a missing id cost the same for halving
for n, hunt, halving in [(7, 7, 3), (70, 70, 7), (700, 700, 10), (7000, 7000, 13)]:
    o = list(range(101, 101 + n))
    assert find(o, 100 + n) == hunt == n
    assert halve_looks(o, 100 + n) == halving
    assert halve_looks(o, 9999) == halving
    assert max(halve_looks(o, x) for x in o) == halving
# doubling adds one look
o = list(range(101, 101 + 14000))
assert halve_looks(o, 100 + 14000) == 14 and max(halve_looks(o, x) for x in o) == 14
# question 1
o = list(range(101, 101 + 56000))
assert 7000 * 2 ** 3 == 56000 and max(halve_looks(o, x) for x in o) == 16 and 16 - 13 == 3 and 56000 - 7000 == 49000
# question 2
def halve(ids, wanted):
    lo, hi = 0, len(ids) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if ids[mid] == wanted:
            return True
        if ids[mid] < wanted:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
u = [104, 101, 107, 102, 106, 103, 105]
assert u[3] == 102 and u[4:] == [106, 103, 105] and u[4:][1] == 103
assert (halve(u, 106), halve(sorted(u), 106)) == (False, True)
# source: https://docs.python.org/3/library/bisect.html
# confirmed: "The module is called bisect because it uses a basic bisection algorithm to do its work", and the sorted-list use (movies.sort(key=by_year) then bisect)
