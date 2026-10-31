# 284: how Postgres keeps a table on disk, rows packed into pages
builds on: [283 capstone, the same lookup three ways, scan, halving and hash](./283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md), [249 MVCC, an update writes a new row version](./249-mvcc-an-update-writes-a-new-row-version.md)
section: inside a database server, part 1, ~2 min read

where does order 106 actually sit inside Postgres, and what does reading just that one row cost? [283](./283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md) was about shortcuts for finding things, so now, where the things live.

Postgres ([211](./211-a-database-server-postgres-where-most-app-data-lives.md), a database that runs as its own server) keeps a table in a file cut into pages: fixed chunks of 8192 bytes, each packed with many rows. a rows address is its page number and its slot, a numbered seat on that page. page here is not a web page or the paging of [120](./120-limit-and-offset-paging-through-rows.md), and this slot is not a hash table slot from [278](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md).

the shop, the imaginary gujarati snack store these notes run on, loaded into Postgres 16, other columns left out. ctid is the hidden address column:

```text
-- Postgres 16
SELECT ctid, order_id, status FROM orders;

 ctid  | order_id | status
 (0,1) |      101 | delivered
 (0,2) |      102 | delivered
 (0,3) |      103 | delivered
 (0,4) |      104 | cancelled
 (0,5) |      105 | delivered
 (0,6) |      106 | pending
 (0,7) |      107 | delivered

page 0, 8192 bytes: | 101 | 102 | 103 | 104 | 105 | 106 | 107 | free |
```

all 7 orders share page 0, and the table file is exactly 8192 bytes. to read only 106 the whole page comes along, the same rule as the [blocks](./044-disks-read-in-blocks.md) of 044 (a page is two 4096 byte blocks on typical linux).

i pictured a table as a long list the server picks rows from one by one, but the unit it moves around is the page, and a row is just a seat on one.

this is the slot of [249](./249-mvcc-an-update-writes-a-new-row-version.md). after Asha sets 106 to delivered, it sits at (0,8) while 107 stays at (0,7), so when you update a row, its address changes. 1000 made up orders took 8 pages.

8 kB is the usual size ([docs](https://www.postgresql.org/docs/current/storage-page-layout.html)).

---
prev: [283 capstone, the same lookup three ways, scan, halving and hash](./283-capstone-the-same-lookup-three-ways-scan-halving-and-hash.md) | next: not written yet
