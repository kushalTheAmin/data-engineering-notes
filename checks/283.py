# checks for notes/283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md
import math
from bisect import bisect_left


def scan(ids, w):
    n = 0
    for i in ids:
        n += 1
        if i == w:
            return n
    return n


def halve(ids, w):
    lo, hi, n = 0, len(ids) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        n += 1
        if ids[mid] == w:
            return n
        if ids[mid] < w:
            lo = mid + 1
        else:
            hi = mid - 1
    return n


def hash_find(slots, w):
    n = 0
    for i in slots[w % len(slots)]:
        n += 1
        if i == w:
            return n
    return n


rows = []
for n in [7, 70, 700, 7000]:
    ids = list(range(101, 101 + n))
    slots = [[] for _ in range(n)]
    for i in ids:
        slots[i % n].append(i)
    rows.append((n, max(scan(ids, w) for w in ids), max(halve(ids, w) for w in ids),
                 max(hash_find(slots, w) for w in ids)))
assert rows == [(7, 7, 3, 1), (70, 70, 7, 1), (700, 700, 10, 1), (7000, 7000, 13, 1)]
# the table: a balanced tree over 7000 ids is about 13 levels deep when perfectly even
assert math.floor(math.log2(7000)) + 1 == 13
# the table and 282: 118348 write steps for 700 mixed up arrivals vs 700 loose (see checks/282.py)
# check yourself 1: 7 million is 7000 times 1000, worst case halving is 23 looks
assert 7000 * 1000 == 7_000_000
assert math.floor(math.log2(7_000_000)) + 1 == 23
assert 2 ** 22 < 7_000_000 < 2 ** 23
assert max(halve(list(range(7_000_000)), w) for w in [0, 1, 3_499_999, 6_999_998, 6_999_999]) == 23
assert 13 * 1000 == 13000
# prose: sorted ids let you find where 500 starts, then walk to 600
ids = list(range(101, 7101))
start = bisect_left(ids, 500)
assert ids[start:start + 101][0] == 500 and ids[start:start + 101][-1] == 600
