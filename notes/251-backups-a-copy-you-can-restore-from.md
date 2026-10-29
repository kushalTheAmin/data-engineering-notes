# 251: backups, a copy you can restore from
builds on: [250 transaction snapshots, what your transaction is allowed to see](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md), [234 replaying the log after a crash](./234-replaying-the-log-after-a-crash.md), [232 durability, surviving a crash](./232-durability-surviving-a-crash.md), [226 DROP and TRUNCATE, emptying a table vs removing it](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md), [103 your first query against the shop](./103-your-first-query-against-the-shop.md)
section: changing data safely, part 44, ~2 min read

Asha runs DROP TABLE orders CASCADE on the live shop database by mistake and commits it. [durability](./232-durability-surviving-a-crash.md) says a kept change survives a crash, so does the drop survive too? yes, and thats the problem.

a backup is a copy of your data, kept somewhere else, that you can restore, meaning load it back to get the data as it was when the copy was taken. [replaying the log](./234-replaying-the-log-after-a-crash.md) (the record of every change) after a crash redoes changes, it never takes one back, so a [DROP](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md) (removing the table itself) stays dropped. CASCADE is there because other tables point at orders, per that note. the shop, the imaginary gujarati snack store these notes run on, has 7 real orders, 108 is imagined:

```python
live = [101, 102, 103, 104, 105, 106, 107]
backup = list(live)
print("02:00 backup taken ", len(backup), "orders")
live.append(108)
print("09:30 order 108 in ", len(live), "live,", len(backup), "in backup")
live = None
print("11:00 DROP TABLE    live gone, backup has", len(backup))
live = list(backup)
print("11:05 restore      ", len(live), "orders, 108 back:", 108 in live)
```

```output
02:00 backup taken  7 orders
09:30 order 108 in  8 live, 7 in backup
11:00 DROP TABLE    live gone, backup has 7
11:05 restore       7 orders, 108 back: False
```

108 came after the 02:00 copy, so the restore cant have it. list(live) makes a real copy, while backup = live would be a second name for one list.

i assumed restore meant undoing the mistake. it only takes you back to the moment of the copy, so Esha was told 108 was saved at 09:30 and now its gone.

so what: Postgres ships pg_dump, which by default writes a [SQL dump](./103-your-first-query-against-the-shop.md) (a text file of commands that rebuilds the database). the docs say it makes consistent exports (matching one moment) while the database is in use, and doesnt block readers or writers, but also that for regular production backups its generally not the right choice. a later note closes the 02:00 to 11:00 gap.

---
prev: [250 transaction snapshots, what your transaction is allowed to see](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md) | next: [252 point in time recovery, a backup plus the replayed log](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md)
