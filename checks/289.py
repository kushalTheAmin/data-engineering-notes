# checks for notes/289-how-a-b-tree-stays-balanced-as-rows-arrive.md
capacity = 3
signposts = [104, 107]
leaves = [[101, 102, 103], [104, 105, 106], [107]]
splits = []
for v in [108, 109, 110]:
    i = sum(1 for s in signposts if v >= s)
    leaves[i].append(v)
    leaves[i].sort()
    if len(leaves[i]) > capacity:
        right = leaves[i][len(leaves[i]) // 2:]
        del leaves[i][len(leaves[i]) // 2:]
        leaves.insert(i + 1, right)
        signposts.insert(i, right[0])
        splits.append(v)
assert splits == [110]
assert signposts == [104, 107, 109]
assert leaves == [[101, 102, 103], [104, 105, 106], [107, 108], [109, 110]]
assert len(leaves) == 4
# first three leaves untouched by the split
assert leaves[:2] == [[101, 102, 103], [104, 105, 106]]
# source: https://www.postgresql.org/docs/16/btree-implementation.html
# confirmed: leaf split moves items to a new page and inserts a new downlink in the parent, splits "cascade upwards", a root split adds a new level above the old root (opened this run)
