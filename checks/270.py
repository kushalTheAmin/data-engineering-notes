# checks for notes/270-flat-and-straight-line-the-two-shapes-of-growth.md
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

# the shop has orders 101 to 107
assert [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY 1").fetchall()] == list(range(101, 108))
for n in [7, 70, 700, 7000]:
    ids = list(range(101, 101 + n))
    assert ids[-1] == 100 + n
    assert find(ids, ids[-1]) == n
    assert 10 * n == n * 10

# counting comparisons: `in` on a missing id and max both look at every item
class C:
    n = 0
    def __init__(s, v): s.v = v
    def __eq__(s, o): C.n += 1; return s.v == o.v
    def __gt__(s, o): C.n += 1; return s.v > o.v
    def __lt__(s, o): C.n += 1; return s.v < o.v
    __hash__ = None
for n in [7, 70]:
    L = [C(i) for i in range(101, 101 + n)]
    C.n = 0; assert (C(9999) in L) is False; assert C.n == n   # missing id: a look per order
    C.n = 0; max(L); assert C.n == n - 1                       # max compares every item with the best so far
# question 3: 700 doubled three times
assert 700 * 2 ** 3 == 5600 and 700 * 3 == 2100
# source: https://docs.python.org/3/faq/design.html
# confirmed: "This makes indexing a list a[i] an operation whose cost is independent of the size of the list or the value of the index."
# source: https://www.postgresql.org/docs/current/indexes-intro.html
# confirmed: without an index "the system would have to scan the entire test1 table, row by row"; with one "it might only have to walk a few levels deep into a search tree"
# source: https://survey.stackoverflow.co/2025/technology
# confirmed: PostgreSQL is the most used database among all survey respondents, 55.6%, so popular is supported
