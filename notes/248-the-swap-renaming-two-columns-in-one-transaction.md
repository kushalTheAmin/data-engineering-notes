# 248: changing a column type without downtime, the swap in one short transaction
builds on: [247 changing a column type without downtime, keeping the new column in sync with new writes](./247-keeping-the-new-column-in-sync-with-a-trigger.md), [246 changing a column type without downtime, add a new column and backfill it in batches](./246-add-a-new-column-and-backfill-it-in-batches.md), [245 changing a column type, the table rewrite and the lock](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [225 ALTER TABLE, adding a column to a table that already has rows](./225-alter-table-adding-a-column-to-a-table-with-rows.md), [093 foreign key](./093-foreign-key.md), [087 primary key](./087-primary-key.md)
section: changing data safely, part 41, ~2 min read

after [247](./247-keeping-the-new-column-in-sync-with-a-trigger.md) the shop has order_id_big (BIGINT, the 8 byte integer) correct for every order, old and new. but the app still asks for order_id. how do you make it use the new column without touching the app?

the swap is renaming the two columns so the big one takes the old name, all inside one transaction. this is Postgres, and the shop is the imaginary gujarati snack store these notes run on.

```text
-- Postgres
BEGIN;
ALTER TABLE orders RENAME COLUMN order_id TO order_id_old;
ALTER TABLE orders RENAME COLUMN order_id_big TO order_id;
COMMIT;
```

| type | name before | name after |
| --- | --- | --- |
| INTEGER | order_id | order_id_old |
| BIGINT | order_id_big | order_id |

i kept waiting for the expensive step, and the swap is just two labels trading places. the docs say a rename has no effect on the stored data, so nothing is copied, unlike the rewrite in [245](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md).

why one [transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (a group of changes that all happen or none do)? i ran the first rename alone on Postgres 16, and SELECT order_id failed with column "order_id" does not exist. Postgres can undo [ALTER TABLE](./225-alter-table-adding-a-column-to-a-table-with-rows.md) too, so inside BEGIN and COMMIT nobody sees that gap.

the catch: a rename takes ACCESS EXCLUSIVE ([245](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md), the lock, a mark making others wait, that blocks even a plain SELECT read). it is held for milliseconds, not for a whole copy.

one more gotcha, the [primary key](./087-primary-key.md) (the unique id column) and the [foreign key](./093-foreign-key.md) (a column pointing at another table) from order_items stay attached to order_id_old. moving them is its own job, so keep that column for now.

### check yourself

1. you run the two renames without BEGIN, each as its own statement. between them, the app runs SELECT * FROM orders WHERE order_id = 107. what happens?

<details><summary>answer</summary>

it fails with column "order_id" does not exist. the first rename already committed, and order_id_big has not been renamed yet. the tempting answer is that it returns order 107 from the old column, but that column has a new name now.

</details>

2. a 20 minute report is mid SELECT on orders when you start the swap. the rename needs ACCESS EXCLUSIVE, so it waits for the report. what do new SELECTs from the shop app do meanwhile? and if lock_timeout caps how long a statement waits for a lock, how does setting it help?

<details><summary>answer</summary>

they wait too, queued behind your rename (i tested this on Postgres 16), so a tiny swap can stall the shop. lock_timeout makes your rename give up instead of queueing, then retry later. the tempting answer is that the app keeps reading, since a rename is tiny.

</details>

---
prev: [247 changing a column type without downtime, keeping the new column in sync with new writes](./247-keeping-the-new-column-in-sync-with-a-trigger.md) | next: not written yet
