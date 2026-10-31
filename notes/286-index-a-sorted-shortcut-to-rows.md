# 286: index, a sorted shortcut to rows
builds on: [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [273 binary search, finding one item in sorted data by halving](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md), [282 the trade off, faster reads usually mean slower writes](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md), [087 primary key](./087-primary-key.md)
section: inside a database server, part 3, ~2 min read

what if a lookup that read 8 pages in [285](./285-full-table-scan-reading-every-page.md) could jump to the right page and read 1 table page instead?

an index is a second list kept next to the table, sorted by one column. each entry is that columns value plus the rows address, the page and slot of [284](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md). to find a value, halve the sorted list like [273](./273-binary-search-finding-one-item-in-sorted-data-by-halving.md) (drop half the sorted items per look), then follow the address. index here is not a list position like numbers[2], and the default index in Postgres (a database server) is sorted.

the shop, the imaginary gujarati snack store these notes run on, here as the 1000 made up orders of 285, 136 rows per page. each entry is (order_id, page, slot):

```python
per_page = 136
table = [(101 + i, i // per_page, i % per_page + 1) for i in range(1000)]
index = sorted(table)

def find(index, want):
    lo, hi, looks = 0, len(index) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        looks += 1
        if index[mid][0] == want:
            return index[mid], looks
        if index[mid][0] < want:
            lo = mid + 1
        else:
            hi = mid - 1

entry, looks = find(index, 1100)
print("scan: 8 pages")
print("index: found", entry, "in", looks, "looks, then read 1 page")
```

```output
scan: 8 pages
index: found (1100, 7, 48) in 10 looks, then read 1 page
```

the entry says page 7, slot 48, so pages 0 to 6 are never read. real rows arrive mixed up, the index is sorted either way.

real Postgres 16 on the same table, pages already cached:

```text
-- Postgres 16
CREATE INDEX orders1000_id_idx ON orders1000 (order_id);

Seq Scan   before:  Buffers: shared hit=8
Index Scan after:   Buffers: shared hit=3
```

3 and not 1, because Postgres stores the index in pages too, as a tree, so 2 index pages plus the table page. a later note opens that tree.

i figured an index was a sorted copy of the table, but its only keys and addresses, and the rows stay put.

Postgres builds one on every [primary key](./087-primary-key.md), so when you look up by key, even a huge table stays fast. every write now updates the index too, a bill like the one in [282](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md).

### check yourself

1. you index the 7 shop orders by customer_id. how many entries does the index hold, and how many sit together under Asha, customer 1?

```sql
SELECT customer_id, count(*) AS entries FROM orders GROUP BY customer_id ORDER BY customer_id;
```

<details><summary>answer</summary>

```result
customer_id | entries
1 | 3
2 | 2
3 | 1
4 | 1
```

7 entries, one per row, and Asha has 3 side by side because the list is sorted. the tempting answer is 4, one per customer, but the index points at rows, not people.

</details>

2. someone asks for order 999999, which doesnt exist. how many table pages does Postgres read with the index, and why not 8?

<details><summary>answer</summary>

none. the sorted index shows where 999999 would sit and finds nothing there, so there is no address to follow. on Postgres 16 the plan showed Buffers: shared hit=2, both index pages. the tempting answer is 8, from 285 where a miss cost a full scan.

</details>

---
prev: [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md) | next: not written yet
