# 253: capstone, placing an order as one transaction
builds on: [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md), [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [233 the write ahead log, write down the plan before the change](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md), [243 SELECT FOR UPDATE, locking on purpose](./243-select-for-update-locking-on-purpose.md), [241 serializable, as if one at a time, and retrying the failures](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md), [252 point in time recovery, a backup plus the replayed log](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md)
section: changing data safely, wrap up, ~3 min read

[252](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md) was the last safety net, a copy plus a kept log for after a mistake. this one goes back to the first tap: Esha presses place order, so what has to be true for that to be safe?

the shop, the imaginary gujarati snack store these notes run on, takes an order as two inserts. here they are for order 108 (imagined, Esha is customer 5, dhokla is product 1), with the note behind each line:

```text
-- Postgres
BEGIN;                                   -- open a group of changes, all or nothing (227, 228)
INSERT INTO orders VALUES (108, 5, TIMESTAMP '2026-04-10 11:00:00', 'pending');
                                         -- add the order row; column rules checked now (215 to 218)
INSERT INTO order_items VALUES (108, 1, 2);
                                         -- add 2 dhokla; a product id that doesnt exist is refused by the foreign key (218)
COMMIT;                                  -- keep both changes (229), after the change list is saved
                                         -- to disk (233), and only then tell Esha done, by default (232)
                                         -- other people see 108 from this moment, not before, at the default level (231)
```

the transaction is the small part, four lines. the rules refuse a bad row and [ROLLBACK](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (throw away every change since BEGIN) undoes the other insert, and [the WAL](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md) (the changes list kept on disk) is flushed before Esha hears done. everything else in this section is a layer around those four lines, and you can follow any row to the note that built it:

| layer | what it gives the order | notes |
| --- | --- | --- |
| the server | Postgres in a container, one session per connection | [208](./208-containers-a-program-packed-with-everything-it-needs.md) [209](./209-images-and-containers-the-packed-box-and-the-running-copy.md) [210](./210-running-postgres-in-a-container-on-your-laptop.md) [211](./211-a-database-server-postgres-where-most-app-data-lives.md) [212](./212-connections-and-sessions-one-conversation-with-the-database.md) |
| the tables | made with CREATE TABLE, scratch copies with TEMP | [213](./213-create-table-naming-a-table-and-its-columns.md) [214](./214-temporary-tables.md) |
| the rules | NOT NULL, UNIQUE, CHECK and keys refuse bad rows | [215](./215-not-null-and-default-required-columns-and-fallback-values.md) [216](./216-unique-no-two-rows-may-share-a-value.md) [217](./217-check-a-rule-every-value-must-pass.md) [218](./218-key-constraints-primary-key-and-references-in-create-table.md) |
| the ids | a sequence can hand out an id like 108 | [219](./219-sequences-where-made-up-ids-come-from.md) |
| the writes | INSERT, UPDATE, DELETE, upsert | [220](./220-insert-adding-rows-and-matching-values-to-columns.md) [221](./221-insert-from-a-select-copying-rows-from-a-query.md) [222](./222-update-changing-rows-and-why-the-where-matters.md) [223](./223-delete-removing-rows-and-what-still-points-at-them.md) [224](./224-upsert-insert-or-update-in-one-statement.md) |
| the shape | ADD COLUMN, DROP, TRUNCATE | [225](./225-alter-table-adding-a-column-to-a-table-with-rows.md) [226](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md) |
| all or nothing | BEGIN, COMMIT, ROLLBACK | [227](./227-transactions-all-or-nothing.md) [228](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) |
| four promises | atomic, consistent, isolated, durable | [229](./229-acid-four-promises-a-database-makes.md) [230](./230-acid-consistency-the-rules-still-hold-after-every-change.md) [231](./231-isolation-two-people-at-the-same-time.md) [232](./232-durability-surviving-a-crash.md) |
| the crash | log first, replay after | [233](./233-the-write-ahead-log-write-down-the-plan-before-the-change.md) [234](./234-replaying-the-log-after-a-crash.md) |
| two at once, the bugs | lost update, dirty read, non repeatable read, phantom | [235](./235-lost-updates.md) [236](./236-dirty-reads.md) [237](./237-non-repeatable-reads.md) [238](./238-phantoms.md) |
| two at once, the levels | read committed, repeatable read, serializable | [239](./239-isolation-levels-read-committed.md) [240](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md) [241](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md) |
| waiting on purpose | row and table locks, FOR UPDATE, deadlocks | [242](./242-row-locks-and-table-locks.md) [243](./243-select-for-update-locking-on-purpose.md) [244](./244-deadlocks-two-transactions-waiting-on-each-other.md) |
| a big change, live | rewrite, backfill, sync, swap | [245](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md) [246](./246-add-a-new-column-and-backfill-it-in-batches.md) [247](./247-keeping-the-new-column-in-sync-with-a-trigger.md) [248](./248-the-swap-renaming-two-columns-in-one-transaction.md) |
| who sees what | row versions and snapshots | [249](./249-mvcc-an-update-writes-a-new-row-version.md) [250](./250-transaction-snapshots-what-your-transaction-is-allowed-to-see.md) |
| after a mistake | backup, then log replay | [251](./251-backups-a-copy-you-can-restore-from.md) [252](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md) |

i used to think the transaction was the whole safety, but its four lines and everything else is layers around them. two shoppers who read the same stock can still need [a lock](./243-select-for-update-locking-on-purpose.md) or [serializable](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md), and a committed drop needs a backup. each layer covers a hole the one before leaves open.

the next section is about designing the tables these inserts go into.

### check yourself

1. Eshas order row goes in with no BEGIN. then she opens a transaction, adds dhokla (good), then khandvi with quantity 0 (CHECK refuses it), and runs ROLLBACK. predict both counts.

```sql
CREATE TABLE my_orders AS SELECT * FROM orders;
CREATE TABLE my_items (order_id INTEGER, product_id INTEGER, quantity INTEGER CHECK (quantity > 0));
INSERT INTO my_orders VALUES (108, 5, TIMESTAMP '2026-04-10 11:00:00', 'pending');
BEGIN;
INSERT INTO my_items VALUES (108, 1, 2)
```

```sql
-- fails on purpose
INSERT INTO my_items VALUES (108, 2, 0)
```

```sql
ROLLBACK;
SELECT (SELECT count(*) FROM my_orders WHERE order_id = 108) AS orders_108, (SELECT count(*) FROM my_items WHERE order_id = 108) AS items_108
```

<details><summary>answer</summary>

```result
orders_108 | items_108
1 | 0
```

the order insert ran before BEGIN, so it was already kept. the tempting 0 and 0 reads ROLLBACK as undoing everything.

</details>

2. imagine one dhokla left in a stock table. Asha and Esha both run BEGIN, then SELECT ... WHERE left_over > 0 FOR UPDATE ([243](./243-select-for-update-locking-on-purpose.md), a read that locks the rows it returns), then, if a row came back, an UPDATE taking 1 off left_over and COMMIT, Asha first, on Postgres defaults. who gets the dhokla?

<details><summary>answer</summary>

Asha. Esha waits for the lock, then Postgres rechecks the WHERE on the row as Asha saved it, finds 0 left, returns no row. the tempting both assumes each saw 1.

</details>

3. a table was dropped at 11:00. you restore a backup and replay the kept log up to 10:59 ([252](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md)), but the log files you kept end at 10:30. does Postgres quietly stop at 10:30?

<details><summary>answer</summary>

no. current docs: recovery ending before the target shuts the server down with a fatal error. the tempting yes assumes the closest point.

</details>

---
prev: [252 point in time recovery, a backup plus the replayed log](./252-point-in-time-recovery-a-backup-plus-the-replayed-log.md) | next: [254 modeling, deciding the tables before writing them](./254-modeling-deciding-the-tables-before-writing-them.md)
