# 244: deadlocks, two transactions waiting on each other
builds on: [243 SELECT FOR UPDATE, locking on purpose](./243-select-for-update-locking-on-purpose.md), [242 row locks and table locks](./242-row-locks-and-table-locks.md), [241 serializable, as if one at a time, and retrying the failures](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md)
section: changing data safely, part 37, ~2 min read

[243](./243-select-for-update-locking-on-purpose.md) made the second person wait on purpose. so what happens when the person you are waiting for is waiting for you?

a deadlock is two [transactions](./227-transactions-all-or-nothing.md) (groups of changes that all happen or none do) that each hold a lock the other one needs, so neither can ever move. this is Postgres, a database that runs as its own server.

the shop, the imaginary gujarati snack store these notes run on, has orders 106 and 107. Asha and Esha each run a cleanup that cancels both, but in opposite order. an UPDATE takes a [row lock](./242-row-locks-and-table-locks.md) (a mark on one row, so others changing it wait):

```text
-- Postgres
asha: BEGIN; UPDATE orders SET status = 'cancelled' WHERE order_id = 106;
esha: BEGIN; UPDATE orders SET status = 'cancelled' WHERE order_id = 107;
asha: UPDATE orders SET status = 'cancelled' WHERE order_id = 107;  -- waits
esha: UPDATE orders SET status = 'cancelled' WHERE order_id = 106;  -- waits

asha --holds--> order 106 <--wants-- esha
esha --holds--> order 107 <--wants-- asha
```

follow the arrows and you end where you started. plain waiting is fine, it ends when the other person [commits](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (keeps their changes). a circle never ends.

i assumed the server would hang until someone restarted it. instead Postgres goes looking: once a lock wait has lasted deadlock_timeout (1 second by default), it checks for a circle. if it finds one it aborts one of the transactions (you cant pick which) with error 40P01, deadlock_detected. that one is [rolled back](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (every change thrown away) and the other goes through.

the fix is boring: lock rows in the same order, 106 then 107. then Esha just waits behind Asha and this circle cant form. the Postgres docs call that the best defense, and add that if you cant guarantee it, retry the aborted transaction, same habit as [241](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md) (rerun on a failure).

### check yourself

1. Asha updates 106 then 107. Esha only ever updates 107, then commits. Esha grabs 107 while Asha is still on 106. do they deadlock?

<details><summary>answer</summary>

no. Asha waits for 107, but Esha wants nothing else, so she commits and Asha carries on. a deadlock needs a circle and here the arrows only go one way. the tempting yes sees two people and two held locks.

</details>

2. your app gets 40P01 on its second UPDATE. it retries only that second UPDATE. whats wrong?

<details><summary>answer</summary>

the abort rolled back the whole transaction, including the first UPDATE. the retry would leave the first out. rerun the whole transaction from BEGIN. the tempting answer is that only the failing statement was undone.

</details>

---
prev: [243 SELECT FOR UPDATE, locking on purpose](./243-select-for-update-locking-on-purpose.md) | next: [245 changing a column type, the table rewrite and the lock](./245-changing-a-column-type-the-table-rewrite-and-the-lock.md)
