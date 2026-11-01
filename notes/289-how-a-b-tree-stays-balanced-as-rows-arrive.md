# 289: how a B tree stays balanced as rows arrive
builds on: [288 one lookup traced through a B tree](./288-one-lookup-traced-through-a-b-tree.md), [287 B tree, pages that point to pages](./287-b-tree-pages-that-point-to-pages.md), [281 balanced trees, why the depth stays small](./281-balanced-trees-why-the-depth-stays-small.md), [282 the trade off, faster reads usually mean slower writes](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md)
section: inside a database server, part 6, ~2 min read

[288](./288-one-lookup-traced-through-a-b-tree.md) walked a finished tree. but orders keep arriving and a page holds so much, so what do you think happens when order 110 lands on a leaf page (a bottom page) with no room left?

the leaf splits. half its entries move to a new page next to it, and the parent page gets one new signpost (a value saying which child to follow) for the new page. nothing else moves.

the shop, the imaginary snack store these notes run on, with the toy tree of [287](./287-b-tree-pages-that-point-to-pages.md): a root over leaves of at most 3 entries. orders 108 to 110 are made up new ones.

```python
capacity = 3
signposts = [104, 107]
leaves = [[101, 102, 103], [104, 105, 106], [107]]

def insert(v):
    i = sum(1 for s in signposts if v >= s)
    leaf = leaves[i]
    leaf.append(v)
    leaf.sort()
    if len(leaf) > capacity:
        right = leaf[len(leaf) // 2:]
        del leaf[len(leaf) // 2:]
        leaves.insert(i + 1, right)
        signposts.insert(i, right[0])
        print("insert", v, "-> leaf full, split, new signpost", right[0])
    else:
        print("insert", v, "-> fits")
    print("  root", signposts, "leaves", leaves)

print("start")
print("  root", signposts, "leaves", leaves)
for v in [108, 109, 110]:
    insert(v)
```

```output
start
  root [104, 107] leaves [[101, 102, 103], [104, 105, 106], [107]]
insert 108 -> fits
  root [104, 107] leaves [[101, 102, 103], [104, 105, 106], [107, 108]]
insert 109 -> fits
  root [104, 107] leaves [[101, 102, 103], [104, 105, 106], [107, 108, 109]]
insert 110 -> leaf full, split, new signpost 109
  root [104, 107, 109] leaves [[101, 102, 103], [104, 105, 106], [107, 108], [109, 110]]
```

108 and 109 fit. 110 finds the right leaf holding 107, 108, 109, so it splits into 107, 108 and 109, 110, and the root gets signpost 109. four leaves now, but a lookup still reads the root and one leaf, and the first two leaves were never touched.

i assumed a full page would make the tree lopsided at the bottom, but it never grows down there, new leaves just appear side by side.

if the root fills up, it splits too, and a new root goes above it. the Postgres docs say splits "cascade upwards" ([docs](https://www.postgresql.org/docs/16/btree-implementation.html)). so every leaf stays the same distance from the top, which is the balance of [281](./281-balanced-trees-why-the-depth-stays-small.md).

the catch is the write bill from [282](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md): the insert that splits also writes a new page and edits its parent, so it costs more than one that fits.

---
prev: [288 one lookup traced through a B tree](./288-one-lookup-traced-through-a-b-tree.md) | next: not written yet
