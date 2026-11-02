# 293: what indexes cost, slower writes and more disk
builds on: [292 covering index, when the index alone has the answer](./292-covering-index-when-the-index-alone-has-the-answer.md), [290 composite indexes, sorted by the first column, then the second](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md), [289 how a B tree stays balanced as rows arrive](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md), [286 index, a sorted shortcut to rows](./286-index-a-sorted-shortcut-to-rows.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [282 the trade off, faster reads usually mean slower writes](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md)
section: inside a database server, part 10, ~2 min read

i put two indexes on the 1000 order table and they came out bigger than the table. how does a shortcut outweigh what it points at?

an index costs you twice: disk, since each index is its own sorted list in its own pages, and writes, since an INSERT usually adds an entry to every index, not just a row to the table. real numbers for the [trade off](./282-the-trade-off-faster-reads-usually-mean-slower-writes.md).

the shop, the imaginary gujarati snack store these notes run on, as the 1000 made up orders of [286](./286-index-a-sorted-shortcut-to-rows.md) (4 columns) in Postgres 16, a database server. one [index](./286-index-a-sorted-shortcut-to-rows.md) on order_id, one [composite index](./290-composite-indexes-sorted-by-the-first-column-then-the-second.md) on (customer_id, ordered_at). a page is the 8192 byte chunk of [284](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md).

```text
-- Postgres 16
table orders1000                      8 pages
index on order_id                     5 pages
index on (customer_id, ordered_at)    6 pages
all together                         19 pages

INSERT one new order, id 1101:
table orders1000                      +1 row
index on order_id                     +1 entry
index on (customer_id, ordered_at)    +1 entry
```

11 pages of index against 8 of table. an entry is the value plus the rows address, 16 and 24 bytes against 56 for a row. add a 4 byte pointer each and spare room in every page, and entries alone fill 7 pages, plus a metapage (a bookkeeping page) and a root page (the top page) per index.

the insert: one new order is three writes in three places, each entry finding its spot in its own tree, sometimes with a [page split](./289-how-a-b-tree-stays-balanced-as-rows-arrive.md).

i assumed an index was a thin layer beside the table, but two took more room than the table.

the Postgres docs say every index must be kept synchronized, which adds overhead to writes, and that indexes seldom or never used should be removed ([docs](https://www.postgresql.org/docs/16/indexes-intro.html)). so adding one is a decision.

### check yourself

1. the shop order_items table has PRIMARY KEY (order_id, product_id). you never created an index on it. how many index entries does Postgres already keep for it?

```sql
SELECT count(*) AS rows_in_order_items FROM order_items;
```

<details><summary>answer</summary>

```result
rows_in_order_items
13
```

13, one entry per row, because Postgres builds an index for every primary key (286). the tempting answer is 0, from counting only indexes you made yourself.

</details>

2. the shop logs every page view, 5000 inserts a minute, and one report a day looks views up by visitor_id. a teammate wants an index on every column. what do you say?

<details><summary>answer</summary>

index visitor_id only. every extra index adds an entry to all 5000 inserts a minute and takes disk, to speed questions nobody asks. the tempting answer is index everything because reads get faster, but only the questions someone actually asks get faster, while every insert pays for all of them.

</details>

---
prev: [292 covering index, when the index alone has the answer](./292-covering-index-when-the-index-alone-has-the-answer.md) | next: [294 selectivity, when an index doesnt help](./294-selectivity-when-an-index-doesnt-help.md)
