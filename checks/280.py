# checks for notes/280-trees-data-that-branches.md
ids = [101, 102, 103, 104, 105, 106, 107]
tree = {104: (102, 106), 102: (101, 103), 106: (105, 107)}

def path(wanted, node=104):
    seen = [node]
    while node != wanted:
        left, right = tree[node]
        node = right if wanted > node else left
        seen.append(node)
    return seen

# finding 107 takes 3 looks: 104, 106, 107
assert path(107) == [104, 106, 107] and len(path(107)) == 3
# those are the middles of the halving in 273
lo, hi, mids = 0, 6, []
while True:
    mid = (lo + hi) // 2
    mids.append(ids[mid])
    if ids[mid] == 107:
        break
    lo = mid + 1
assert mids == [104, 106, 107]
# untouched: 102, 101, 103, 105
assert set(ids) - set(path(107)) == {101, 102, 103, 105}
# 7 nodes in 3 levels, the walk from 269 needs 7 looks
assert len(ids) == 7 and len(ids) == 1 + 2 + 4
# source: https://www.postgresql.org/docs/current/indexes-types.html
# confirmed: CREATE INDEX creates B-tree indexes by default
