# checks for notes/281-balanced-trees-why-the-depth-stays-small.md
import math

def add(root, v):
    if root is None:
        return [v, None, None]
    node = root
    while True:
        side = 1 if v < node[0] else 2
        if node[side] is None:
            node[side] = [v, None, None]
            return root
        node = node[side]

def looks(root, v):
    n = 0
    while root is not None:
        n += 1
        if v == root[0]:
            return n
        root = root[1] if v < root[0] else root[2]
    return n

def build(ids):
    root = None
    for v in ids:
        root = add(root, v)
    return root

assert looks(build([101, 102, 103, 104, 105, 106, 107]), 107) == 7
assert looks(build([104, 102, 106, 101, 103, 105, 107]), 107) == 3
assert looks(build(range(101, 801)), 800) == 700
# check yourself 1
assert looks(build([105, 106, 107]), 107) == 3
assert looks(build([106, 105, 107]), 107) == 2
# 700 orders balanced: at most 10 looks, same as the table in 273
assert math.ceil(math.log2(700 + 1)) == 10
# 101 102 103 chain has 3 levels, moving 102 up gives 2 levels
assert looks(build([102, 101, 103]), 103) == 2 and looks(build([101, 102, 103]), 103) == 3
# source: https://www.postgresql.org/docs/current/btree.html
# confirmed: PostgreSQL includes an implementation of the standard btree (multi-way balanced tree) index
