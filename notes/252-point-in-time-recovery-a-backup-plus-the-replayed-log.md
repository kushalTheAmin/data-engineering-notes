# 252: point in time recovery, a backup plus the replayed log
builds on: [251 backups, a copy you can restore from](./251-backups-a-copy-you-can-restore-from.md), [234 replaying the log after a crash](./234-replaying-the-log-after-a-crash.md), [233 the write ahead log, write down the plan before the change](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md), [226 DROP and TRUNCATE, emptying a table vs removing it](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md)
section: changing data safely, part 45, ~2 min read

the 02:00 backup from [251](./251-backups-a-copy-you-can-restore-from.md) (a copy of the data kept elsewhere) cant bring back order 108, because it came in at 09:30. but the shop, the imaginary gujarati snack store these notes run on, took that order, so someone wrote it down. where?

in the write ahead log, [WAL](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md), the databases own list of every change, if you kept it. point in time recovery, PITR, means restore the backup, then [replay](./234-replaying-the-log-after-a-crash.md) (redo from the log) forward and stop at a time you pick. this is Postgres, a database run as its own server, and the backup has to be a file copy of its data, not a SQL dump. 108 is imagined, 106 is a real pending shop order, each log record is one change:

| log record | time | change | table if you stop after it |
| --- | --- | --- | --- |
| backup | 02:00 | copy taken | 7 orders, 106 pending |
| 1 | 09:30 | INSERT order 108 | 8 orders, 106 pending |
| 2 | 10:15 | UPDATE order 106 to delivered | 8 orders, 106 delivered |
| 3 | 11:00 | [DROP TABLE orders CASCADE](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md) | no orders table |

```text
-- Postgres, in the recovery settings
restore_command = 'cp /mnt/archive/%f %p'
recovery_target_time = '2026-04-10 10:59:00+00'
```

restore_command is what Postgres runs to fetch a kept log file (cp copies a file, %f is its name, %p where it goes). recovery_target_time is where to stop, +00 meaning UTC. records 1 and 2 get redone, record 3 never runs, so 108 is back and 106 shows delivered, which the backup alone doesnt have.

i assumed the log only mattered during a crash, but here its the thing you keep.

so what: you keep it on purpose, copying each log file out once its full (Postgres calls that archiving), so you only recover as far as the last file copied. the docs say that if the files run out before your stop time, Postgres shuts down with an error.

---
prev: [251 backups, a copy you can restore from](./251-backups-a-copy-you-can-restore-from.md) | next: not written yet
