# 285: full table scan, reading every page
builds on: [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [283 capstone, the same lookup three ways, scan, halving and hash](./283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md), [270 flat and straight line, the two shapes of growth](./270-flat-and-straight-line-the-two-shapes-of-growth.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [087 primary key](./087-primary-key.md)
section: inside a database server, part 2, ~2 min read

order 106 sits in the 6th row of a table, and Postgres, a database that runs as its own server, still read all 8 pages. why didnt it stop? [284](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) said a table is pages, 8192 byte chunks packed with rows, numbered from 0.

a full table scan reads every page of a table in order and tests the [WHERE](./106-where-keeping-only-the-rows-that-match.md) condition on every row. its the scan of [283](./283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md), counted in pages.

the shop, the imaginary gujarati snack store these notes run on, has 7 orders, here padded to 1000 made up ones. its a copy with no [primary key](./087-primary-key.md) (a column unique in every row), so no shortcut exists. EXPLAIN shows the steps Postgres picks, and ANALYZE really runs them:

```text
-- Postgres 16
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY OFF)
SELECT * FROM orders1000 WHERE order_id = 106;

 Seq Scan on orders1000 (actual rows=1 loops=1)   <- the scan, 1 row came out
   Filter: (order_id = 106)                       <- the if, run on every row
   Rows Removed by Filter: 999                    <- checked and thrown away
   Buffers: shared hit=8                          <- pages touched, all 8
```

the same table, three questions:

| query | pages touched | rows thrown away |
|---|---|---|
| WHERE order_id = 106 | 8 | 999 |
| WHERE order_id = 999999 (not there) | 8 | 1000 |
| WHERE order_id = 106 LIMIT 1 | 1 | 5 |

nothing says order ids are unique in this copy, so a second 106 could sit on page 7, and a miss costs the same 8 pages. only [LIMIT 1](./120-limit-and-offset-paging-through-rows.md) (stop after one row) lets it quit early, because one match is all it needs.

i assumed Postgres would stop at the first match, but without a LIMIT it reads to the end, since it cant know it has them all.

pages touched grow as fast as the table, the straight line of [270](./270-flat-and-straight-line-the-two-shapes-of-growth.md): 100000 similar rows fill 640 pages. you can spot a Seq Scan on a big table returning one row. its not always bad though, Postgres scans the 7 real orders too, since one page needs no shortcut.

### check yourself

1. a table fills 800 pages and its 3 cancelled orders all sit on page 0. how many pages does `WHERE status = 'cancelled'` touch, and how many with `LIMIT 1` added?

<details><summary>answer</summary>

800, then 1. with no LIMIT the scan cant know there are only 3 matches, so it reads every page. with LIMIT 1 it quits at the first match on page 0. the tempting answer for the first is 1, from thinking the matches are up front so the work is too.

</details>

2. the 7 shop orders have 5 delivered, 1 cancelled and 1 pending. Postgres scans them for `WHERE status = 'delivered'`. what do Rows Removed by Filter and Buffers say?

```sql
SELECT count(*) AS removed FROM orders WHERE status <> 'delivered';
```

<details><summary>answer</summary>

```result
removed
2
```

removed is 2 and Buffers is 1 page, since all 7 orders share page 0. 5 rows come out and the other 2 are thrown away. the tempting answer is 7 removed, from counting every row checked, but removed only counts the ones that failed the filter.

</details>

---
prev: [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) | next: not written yet
