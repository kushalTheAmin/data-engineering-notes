# 249: MVCC, an update writes a new row version
builds on: [248 changing a column type without downtime, the swap in one short transaction](./248-the-swap-renaming-two-columns-in-one-transaction.md), [242 row locks and table locks](./242-row-locks-and-table-locks.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md)
section: changing data safely, part 42, ~2 min read

Asha is mid UPDATE (a command that changes a row) on order 106 and hasnt committed yet. Esha reads 106 and gets an answer with no waiting, as [242](./242-row-locks-and-table-locks.md) showed. what is she reading, if the row is being changed?

the answer is MVCC, multi version concurrency control: Postgres (a database that runs as its own server) never overwrites a row. an UPDATE writes a new copy, a row version, and stamps the old one as ended. every version carries two stamps: xmin, the id of the [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) that created it, and xmax, the one that ended it, 0 while it is current.

the shop, the imaginary snack store these notes run on: Ashas transaction 739 updates order 106 to delivered. afterwards, a slice from my own run (slot is the copys position in storage):

```text
-- Postgres 16, stored row versions (a slice)
slot  order  status     xmin  xmax
6     106    pending    738   739
7     107    delivered  738   0
8     106    delivered  739   0
```

| who | while 739 is open | after 739 commits, her next query |
| --- | --- | --- |
| asha | slot 8, delivered | slot 8, delivered |
| esha | slot 6, pending | slot 8, delivered |

i assumed UPDATE worked like d["status"] = "delivered" on a dictionary. its closer to appending a new dictionary to the list and crossing out the old one. the table holds 8 versions for 7 orders, and Esha reads slot 6, so she never waits. the xmax stamp is already on it, but it only counts once 739 [commits](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (becomes permanent).

so what: the Postgres docs say reading never blocks writing and writing never blocks reading (a table lock like the rename in [248](./248-the-swap-renaming-two-columns-in-one-transaction.md) still can). the price is old versions piling up until VACUUM, a cleanup job autovacuum runs for you, removes ones nobody can see.

### check yourself

1. on the original shop table, no earlier updates, Asha updates order 106 to cancelled, then runs ROLLBACK (throw the changes away). how many versions of order 106 are stored now, and which status does a new SELECT read?

<details><summary>answer</summary>

two versions, pending and cancelled, and a SELECT reads pending. the cancelled copy was written, but its creator never committed, so readers skip it and nothing needs undoing. the tempting one version thinks ROLLBACK erases the copy at once, but VACUUM does that later.

</details>

2. on a fresh copy of the shop table (7 versions, no earlier updates), Esha runs UPDATE orders SET status = status, which sets every order to the status it already has. SELECT count(*) still says 7. how many versions are stored right after?

<details><summary>answer</summary>

14, the 7 old versions plus 7 new ones (i counted 14 on Postgres 16). an UPDATE writes a new version even when the value is identical. the tempting 7 assumes nothing is written when nothing changes.

</details>

---
prev: [248 changing a column type without downtime, the swap in one short transaction](./248-the-swap-renaming-two-columns-in-one-transaction.md) | next: [250 transaction snapshots, what your transaction is allowed to see](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md)
