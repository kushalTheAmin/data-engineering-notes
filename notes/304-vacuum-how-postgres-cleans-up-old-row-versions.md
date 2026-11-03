# 304: vacuum, how Postgres cleans up old row versions
builds on: [303 the buffer pool, keeping hot pages in memory](./303-the-buffer-pool-keeping-hot-pages-in-memory.md), [284 how Postgres keeps a table on disk, rows packed into pages](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md), [250 transaction snapshots, what your transaction is allowed to see](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md), [249 MVCC, an update writes a new row version](./249-mvcc-an-update-writes-a-new-row-version.md)
section: inside a database server, part 21, ~2 min read

i deleted a row from Postgres (a database that runs as its own server), SELECT count(*) said it was gone, and its bytes were still on disk. [303](./303-the-buffer-pool-keeping-hot-pages-in-memory.md) kept pages in memory, so when does a deleted row really leave one?

an UPDATE or DELETE never erases a row, it ends it, as [249](./249-mvcc-an-update-writes-a-new-row-version.md) showed. each stored copy, a row version, has xmin and xmax, the ids of the [transaction](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md) (a group of changes) that created it and ended it. a dead row version is an ended one no open transaction could still need, and VACUUM frees those. autovacuum, a background job, runs it for you.

the shop, the imaginary gujarati snack store these notes run on, as an orders-only copy. a slot is a numbered seat on a page, an 8192 byte chunk of the table file ([284](./284-how-postgres-keeps-a-table-on-disk-rows-packed-into-pages.md)). Esha opens a repeatable read transaction (one fixed view of the data) and runs a query, then cancelled order 104 is deleted. Postgres 16, my run, ids differ from 249:

| step | slot 4 holds | table file |
| --- | --- | --- |
| DELETE 104 | order 104, xmin 737, xmax 738 | 8192 bytes |
| VACUUM, Esha still open | same, "1 are dead but not yet removable" | 8192 bytes |
| Esha commits, VACUUM again | free | 8192 bytes |
| INSERT order 108 | order 108, at (0,4), page 0 slot 4 | 8192 bytes |

Esha could still see 104, so the first VACUUM left it. the second freed the seat and 108 took it. the file never shrank: plain VACUUM marks space for reuse, while VACUUM FULL rewrites the file smaller ([docs](https://www.postgresql.org/docs/16/routine-vacuuming.html)).

i assumed DELETE meant the bytes were gone, but the row is only hidden, then removable by a later VACUUM once nobody could need it. so a repeatable read transaction left open for days blocks cleanup of rows ended since.

### check yourself

1. page 0 holds orders 101 to 107 in slots 1 to 7. someone deletes 104 and 105, nobody has a transaction open, VACUUM runs, then orders 108 and 109 are inserted. at which addresses (page, slot) do they land? an orders-only copy, so no other tables block the deletes.

<details><summary>answer</summary>

(0,4) and (0,5), the two freed seats (i got that on Postgres 16). the tempting (0,8) and (0,9) treats a table like a list that only appends, but VACUUM made those seats reusable.

</details>

2. an analyst opens a repeatable read transaction on Monday, runs a query, and forgets it. all week the shop updates orders and autovacuum keeps running. what happens to the table file, and does committing that transaction on Friday shrink it?

<details><summary>answer</summary>

it grows, because versions that ended after Monday snapshot are not removable while it lives. committing lets the next VACUUM free them for reuse, but the file normally keeps its size. the tempting yes thinks cleanup returns disk space, which plain VACUUM mostly doesnt.

</details>

---
prev: [303 the buffer pool, keeping hot pages in memory](./303-the-buffer-pool-keeping-hot-pages-in-memory.md) | next: not written yet
