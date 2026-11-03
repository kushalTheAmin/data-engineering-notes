# 303: the buffer pool, keeping hot pages in memory
builds on: [302 EXPLAIN ANALYZE, the planners guesses vs what really happened](./302-explain-analyze-the-planners-guesses-vs-what-really-happened.md), [285 full table scan, reading every page](./285-full-table-scan-reading-every-page.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
section: inside a database server, part 20, ~2 min read

the same query on the same 8 pages said read=8 the first time and hit=8 the second. in [285](./285-full-table-scan-reading-every-page.md) i printed hit=8 and moved on, so what is a hit?

the buffer pool is a chunk of [memory](./036-memory-vs-disk.md) (the working space that forgets at power off) where [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md), a database server, keeps copies of the [pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md) (8192 byte chunks of a table file) it already fetched. it looks there first. found is a hit. missing is a read from disk, which leaves a copy behind, and that trip was [1500 times slower](./037-disk-is-slow.md) than memory on an SSD.

a toy pool of 3 pages, six page requests for the orders table of the shop, the imaginary gujarati snack store these notes run on:

```python
SIZE = 3
pool = []  # pages in memory, least recently used first
hits = reads = 0
for page in [0, 1, 2, 0, 3, 1]:
    if page in pool:
        pool.remove(page)
        pool.append(page)
        hits += 1
        print(f"page {page}: hit, no disk trip. pool {pool}")
    else:
        note = ""
        if len(pool) == SIZE:
            note = f", dropped page {pool.pop(0)}"
        pool.append(page)
        reads += 1
        print(f"page {page}: read from disk{note}. pool {pool}")
print(f"{hits} hit, {reads} reads")
```

```output
page 0: read from disk. pool [0]
page 1: read from disk. pool [0, 1]
page 2: read from disk. pool [0, 1, 2]
page 0: hit, no disk trip. pool [1, 2, 0]
page 3: read from disk, dropped page 1. pool [2, 0, 3]
page 1: read from disk, dropped page 2. pool [0, 3, 1]
1 hit, 5 reads
```

page 0 came back free. then page 3 arrived with the pool full, so the page unused longest was dropped, and wanting page 1 again cost a second trip. real Postgres uses a cheaper rule.

the query from 285, reading all 8 pages, run twice right after a restart:

```text
-- Postgres 16
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF, SUMMARY OFF)
SELECT * FROM orders1000 WHERE order_id = 106;

run 1:  Buffers: shared read=8 ...   <- 8 pages fetched from disk
run 2:  Buffers: shared hit=8        <- same 8 pages, found in the pool
```

shared means ordinary table and index pages. the setting shared_buffers sizes the pool, 128MB by default ([docs](https://www.postgresql.org/docs/16/runtime-config-resource.html)), which is 16384 pages. read means not in the pool, but the operating system keeps its own cache, so it isnt always a real drive trip.

what surprised me is that a restart makes Postgres slower at first, since the pool starts empty. so when you time a query, run it twice.

---
prev: [302 EXPLAIN ANALYZE, the planners guesses vs what really happened](./302-explain-analyze-the-planners-guesses-vs-what-really-happened.md) | next: [304 vacuum, how Postgres cleans up old row versions](./304-vacuum-how-postgres-cleans-up-old-row-versions.md)
