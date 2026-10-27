# 233: the write ahead log, write down the plan before the change
builds on: [232 durability, surviving a crash](./232-durability-surviving-a-crash.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md), [043 reading start to end vs jumping to a spot](./043-reading-start-to-end-vs-jumping.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md)
section: changing data safely, part 26, ~2 min read

Esha gets "done" for order 108 at the shop, the imaginary snack store these notes run on. is 108 in the table file, where the rows live, by then? in [232](./232-durability-surviving-a-crash.md) what got [flushed](./232-durability-surviving-a-crash.md) (forced onto disk) was a log of the change, not the table. why?

the write ahead log, WAL for short, is the databases own list of changes, added to at the end. its one rule: a change goes into the WAL and is flushed before it may go into the table files. this is about Postgres, a database run as its own server.

| step | WAL on disk | table file on disk | Esha told done |
| --- | --- | --- | --- |
| [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (keep my changes) arrives | no 108 | no 108 | no |
| WAL flushed | 108 | no 108 | yes, now |
| table file catches up | 108 | 108 | yes |

look at the middle row. Esha has her done, and if the power died there, 108 would sit on disk in one place only, the WAL. i assumed the table file was the real copy and the log a side note, but at that moment its the other way round.

why bother, you ask? the WAL grows at the end of one file, so its [reading start to end](./043-reading-start-to-end-vs-jumping.md) style, one append. updating the table means [jumping](./043-reading-start-to-end-vs-jumping.md) to whichever [blocks](./044-disks-read-in-blocks.md) (fixed chunks a disk handles whole) hold the rows, and [037](./037-disk-is-slow.md) priced a random lookup at 10 milliseconds on a spinning disk (an SSD gap is smaller). Postgres docs agree.

caveat: the rule is about order. Postgres may write a table page early, just never before the WAL has that change.

if the table file is behind, the WAL still has 108. getting it back is the next one.

### check yourself

1. orders 101 to 103 commit at the same moment. each order has 2 item rows (the query counts them); pretend every item row lands in its own table block. how many table block writes must finish before the last "done" goes out, and how many would a database with no WAL need?

```sql
SELECT count(*) AS item_rows FROM order_items WHERE order_id IN (101, 102, 103)
```

<details><summary>answer</summary>

```result
item_rows
6
```

with a WAL, 0 table writes before done, only the log flush (the table catches up later). without one, all 6 blocks, since the table file is the only copy. the tempting answer is 6 for both, from forgetting the WAL already holds every change.

</details>

2. from [232](./232-durability-surviving-a-crash.md): with the setting synchronous_commit off, Postgres says done without waiting for the WAL flush. does the table file now get written before the WAL record?

<details><summary>answer</summary>

no. only the wait for done is skipped, the order rule stays. thats why the docs say a crash can lose the last few commits but not corrupt anything. the tempting yes assumes off removes the log first rule.

</details>

---
prev: [232 durability, surviving a crash](./232-durability-surviving-a-crash.md) | next: not written yet
