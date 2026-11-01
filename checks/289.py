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
# 'half' is only the toy: Postgres leaves the old leaf about 90 percent full when the new key is the biggest yet
# source: https://www.postgresql.org/docs/16/sql-createindex.html
# confirmed: for B-trees, leaf pages are filled to the fillfactor (default 90) during builds and also when extending the index at the right (adding new largest key values)
# source: https://www.postgresql.org/docs/16/btree-implementation.html
# confirmed: a page split moves "a portion of the items" to a new page, not necessarily half
# rerun this audit on Postgres 16.15: 2000 ascending ids inserted into a primary key, leaf pages bt_page_stats live_items 367, 367, 367, 367, 367, 170 (366 real entries each plus a high key, page capacity about 407), so full left leaves, not half
assert round(407 * 0.9) == 366
# audit: root is first used without a gloss in this note; it now says root (the top page), the same word 287 uses for the top page
