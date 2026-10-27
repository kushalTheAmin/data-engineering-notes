# 234: replaying the log after a crash
builds on: [233 the write ahead log, write down the plan before the change](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md), [232 durability, surviving a crash](./232-durability-surviving-a-crash.md), [044 disks read in blocks, never single bytes](./044-disks-read-in-blocks.md)
section: changing data safely, part 27, ~2 min read

the power dies just after Esha at the shop, the imaginary snack store these notes run on, was told done for order 108. on restart the table file, where rows live on disk, is missing some recent changes. who fixes it?

replaying is how. Postgres, a database run as its own server, keeps a [WAL](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md), a log of every change, saved to disk before the table file is touched. on startup it reads that log forward from a spot it noted earlier and redoes what the table file lacks. thats [durability](./232-durability-surviving-a-crash.md), the promise a change survives a crash, paying off. a slice as a loop, where applied is the last log number the table has. 108 is imagined, 106 is a real pending shop order:

```python
wal = [
    (1, "insert", 108, "pending"),
    (2, "update", 106, "delivered"),
]
# the table file after the crash: it got record 1 but not record 2
table = [[106, "pending"], [108, "pending"]]
applied = 1

for number, kind, order_id, status in wal:
    if number <= applied:
        print(number, "skip, table already has it")
        continue
    if kind == "insert":
        table.append([order_id, status])
    else:
        for row in table:
            if row[0] == order_id:
                row[1] = status
    applied = number
    print(number, "redo", kind, order_id)
print(table)
```

```output
1 skip, table already has it
2 redo update 106
[[106, 'delivered'], [108, 'pending']]
```

record 1 was already in the table file, so replay skips it. i assumed replay meant running the whole log again blindly, but every record first gets one question: do you already have this? in my toy, redoing record 1 would add 108 twice.

how does it know? Postgres stamps each page (its name for a block, 8 kB by default) with the position of the last log record applied to it, and Postgres normally skips a record when the page is already at or past it (source: transam/README). my loop uses one number for the whole table.

so what: a crashed Postgres usually replays for a bit and carries on with no manual repair, unless the log or disk is damaged.

---
prev: [233 the write ahead log, write down the plan before the change](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md) | next: not written yet
