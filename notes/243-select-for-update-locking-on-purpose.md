# 243: SELECT FOR UPDATE, locking on purpose
builds on: [242 row locks and table locks](./242-row-locks-and-table-locks.md), [239 isolation levels, read committed](./239-isolation-levels-read-committed.md), [235 lost updates](./235-lost-updates.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md)
section: changing data safely, part 36, ~2 min read

Asha and Esha both open order 106, see it pending, and both send the delivery email. the customer gets two. [242](./242-row-locks-and-table-locks.md) said a [row lock](./242-row-locks-and-table-locks.md) (a mark so others changing that row wait) stops this, so where was it?

a plain SELECT takes no row lock, so nothing stopped the second reader. SELECT ... FOR UPDATE is a read that also locks every row it returns, until the [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) ends. this is Postgres, the database that runs as its own server. same shape of bug as [235](./235-lost-updates.md): check, then act, with a gap between.

the shop, the imaginary gujarati snack store these notes run on, has order 106 pending. both run this, Asha a split second ahead:

```text
-- Postgres
BEGIN;
SELECT order_id, status FROM orders
WHERE order_id = 106 AND status = 'pending' FOR UPDATE;
-- row came back? send the email, then:
UPDATE orders SET status = 'delivered' WHERE order_id = 106;
COMMIT;
```

| step | asha | esha |
|---|---|---|
| 1 | gets row 106, now locked | (not started) |
| 2 | sends email, UPDATE | same query, waits |
| 3 | COMMIT, lock released | still waiting |
| 4 | done | lock freed, finds 0 rows, sends nothing |

i expected Esha to get the row back and see delivered. she gets nothing instead, because at the default [read committed](./239-isolation-levels-read-committed.md) level Postgres rechecks the WHERE (the filter) against the row as Asha just saved it, and 106 no longer says pending.

the check and the lock happen as one step, so the gap is gone. the catch: with no BEGIN, Postgres runs each statement as its own transaction, so if you forget it the lock is gone the moment the SELECT finishes.

### check yourself

1. a dev adds FOR UPDATE to the SELECT, but their app sends no BEGIN, so the SELECT and the UPDATE go as two separate statements. does the double email still happen?

<details><summary>answer</summary>

yes. each statement is its own transaction, so the lock ends with the SELECT and Esha can read 106 as pending before Asha updates. the tempting no assumes FOR UPDATE locks until the UPDATE, but it only locks until the transaction ends.

</details>

2. Asha runs the query below with FOR UPDATE added, inside a transaction she leaves open. does Esha changing order 107 (delivered) wait?

```sql
SELECT order_id FROM orders WHERE status = 'pending'
```

<details><summary>answer</summary>

```result
order_id
106
```

no. only the rows the query returns get locked, and 107 is delivered, so Esha goes straight through. the tempting yes thinks FOR UPDATE locks the whole table.

</details>

---
prev: [242 row locks and table locks](./242-row-locks-and-table-locks.md) | next: not written yet
