# 288: one lookup traced through a B tree
builds on: [287 B tree, pages that point to pages](./287-b-tree-pages-that-point-to-pages.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [087 primary key](./087-primary-key.md)
section: inside a database server, part 5, ~2 min read

[287](./287-b-tree-pages-that-point-to-pages.md) drew the index (a sorted list of keys and row addresses) as a root page, the top one, over 3 leaf pages, the bottom ones, but never walked it. so when you ask Postgres, a database server, for order 500, which pages (8192 byte chunks of disk) does it touch, and in what order?

a lookup is a walk down. read the root, compare against its signposts (values saying which child to follow), pick a child. read that leaf and halve inside it like [273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) (drop half the sorted items per look) until the entry shows up. then follow the entry address, a page and slot as in [284](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), to the table.

the shop, the imaginary gujarati snack store these notes run on, as the 1000 made up orders of [286](./286-index-a-sorted-shortcut-to-rows.md), 136 rows per page, with the tree of 287:

```python
per_page = 136
signposts = [467, 833]
leaves = [list(range(101, 467)), list(range(467, 833)), list(range(833, 1101))]
want = 500

child = sum(1 for s in signposts if want >= s)
print("read 1, root: signposts", signposts, "so", want, "goes to the", ["left", "middle", "right"][child], "leaf")

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
page, slot = (want - 101) // per_page, (want - 101) % per_page + 1
print("read 2, leaf of", len(leaf), "entries:", looks, "looks, found", (want, page, slot))
print("read 3, table page", page, "slot", slot)
```

```output
read 1, root: signposts [467, 833] so 500 goes to the middle leaf
read 2, leaf of 366 entries: 8 looks, found (500, 2, 128)
read 3, table page 2 slot 128
```

500 is at least 467 and under 833, so the middle leaf. inside it, 8 looks. the entry says table page 2, slot 128, and that is read 3, the same 3 pages Postgres touched in 286. a page not in memory is a slow trip to disk.

i figured the 8 looks would be the worry, but they happen inside a loaded page, so only the 3 page reads count. a signpost value belongs to the side above it, so 467 goes middle too.

this runs under [primary key](./087-primary-key.md) (the column naming each row) lookups on big tables, not the 7 real orders.

### check yourself

1. the toy tree of 287 has a root with signposts 104 and 107, and leaves of at most 3 entries. which leaves hold orders 103 to 105?

```sql
SELECT order_id FROM orders WHERE order_id BETWEEN 103 AND 105 ORDER BY order_id;
```

<details><summary>answer</summary>

```result
order_id
103
104
105
```

two leaves, 103 sits in the left one and 104 and 105 in the middle one. the tempting answer is 1, from thinking three orders in a row must share a leaf.

</details>

2. a toy index page points to 300 pages below it (so two levels reach 300 times 300 leaf entries), and the shop has 20 million orders. how many pages does one lookup read at most, table page included?

<details><summary>answer</summary>

four. two index levels hold only 90000 orders, three hold 27 million, so 3 index pages plus the table page. the tempting answer is 3, forgetting the table page that the address leads to.

</details>

---
prev: [287 B tree, pages that point to pages](./287-b-tree-pages-that-point-to-pages.md) | next: [289 how a B tree stays balanced as rows arrive](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md)
