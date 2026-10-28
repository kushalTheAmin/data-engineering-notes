# 242: row locks and table locks
builds on: [241 serializable, as if one at a time, and retrying the failures](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md), [235 lost updates](./235-lost-updates.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [226 DROP and TRUNCATE, emptying a table vs removing it](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md)
section: changing data safely, part 35, ~2 min read

Asha has changed order 106 and hasnt committed. Esha changes order 107 and it goes straight through, but when she touches 106 her screen just hangs. why only that one row?

a lock is a mark a [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) puts on something so others must wait. a row lock sits on one row, a table lock on the whole table. this is Postgres, the database that runs as its own server, and its UPDATE takes the row lock by itself.

the shop, the imaginary gujarati snack store these notes run on, has orders 106 (pending) and 107 (delivered). Asha ran `UPDATE orders SET status = 'delivered' WHERE order_id = 106` and keeps her transaction open. what Esha runs next:

| asha holds | esha tries | does esha wait? |
|---|---|---|
| row lock on 106 | UPDATE order 106 | yes, until Asha ends her transaction |
| row lock on 106 | UPDATE order 107 | no |
| row lock on 106 | SELECT order 106 | no, she sees the old committed value |
| table lock from DROP TABLE orders | SELECT order 106 | yes, even a plain read waits |

i assumed a lock meant nobody could look, but the docs say row locks block only writers of the same row, never readers. thats the wait behind [235](./235-lost-updates.md): the second UPDATE sits there until the first one [COMMITs or ROLLBACKs](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md). the strongest table lock is what [DROP TABLE](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md) takes, and the docs say only that kind blocks a plain SELECT.

so what: locks are normally held until the transaction ends, so a forgotten COMMIT keeps your row locked for everyone who needs to change it.

---
prev: [241 serializable, as if one at a time, and retrying the failures](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md) | next: [243 SELECT FOR UPDATE, locking on purpose](./243-select-for-update-locking-on-purpose.md)
