# 241: serializable, as if one at a time, and retrying the failures
builds on: [240 repeatable read, rows dont change under you mid transaction](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md), [239 isolation levels, read committed](./239-isolation-levels-read-committed.md), [235 lost updates](./235-lost-updates.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
section: changing data safely, part 34, ~2 min read

Asha and Esha each check the rule "never cancel the last pending order", each follow it, and the rule still breaks. [240](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md) gave each of them a frozen picture of the data, so why isnt that enough?

serializable is the strictest [isolation level](./239-isolation-levels-read-committed.md) (how much of others work a [transaction](./227-transactions-all-or-nothing.md) sees): the result must match some order of running the transactions one at a time. in Postgres, a database that runs as its own server, you pick it with BEGIN ISOLATION LEVEL SERIALIZABLE.

the shop, the imaginary gujarati snack store these notes run on, really has one pending order, 106. pretend 108 is pending too, imagined. each person first counts the pending orders, then cancels one:

| step | who does | repeatable read | serializable |
|---|---|---|---|
| 1 | asha counts pending | 2 | 2 |
| 2 | esha counts pending | 2 | 2 |
| 3 | asha cancels 106, [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (save it) | ok | ok |
| 4 | esha cancels 108, COMMIT | ok | error 40001 (here) |
| 5 | pending orders left | 0 | 1 |

they changed different rows, so theres no [lost update](./235-lost-updates.md) (two writes from one old value) and nothing to block. each decision was fair for the picture it had. but one at a time, Esha would have counted 1 and stopped. serializable catches that and fails one of them with a serialization failure, code 40001. the docs say its hard to predict which one, Esha just commits second here.

i figured strict meant waiting in line, but it lets both run and sends one back at the door. the app must start that whole transaction again, count included, and the retry counts 1 and stops.

so what: the docs say apps here must be ready to retry, so wrap it in a retry loop.

### check yourself

1. Esha gets error 40001. her code reruns only the cancel of 108, reusing her old count of 2. with 106 now cancelled, what count should she have seen, and what should she do? (count(*) counts rows, WHERE keeps only matching rows, <> means not equal)

```sql
SELECT count(*) AS pending FROM orders WHERE status = 'pending' AND order_id <> 106
```

<details><summary>answer</summary>

```result
pending
0
```

the real table has 0 pending once 106 is gone, plus imagined 108 makes 1. a full rerun counts 1 and stops. reusing the old 2, or answering 0 from the query alone, both miss that.

</details>

2. a team moves from repeatable read to serializable and error 40001 shows up in logs, even for transactions touching different rows. a bug in Postgres?

<details><summary>answer</summary>

no. serializable checks what each transaction read, not only what it wrote, so different rows can still clash, and the docs say it can also fail one that would have been fine. the tempting bug theory assumes errors need the same row.

</details>

---
prev: [240 repeatable read, rows dont change under you mid transaction](./240-repeatable-read-rows-dont-change-under-you-mid-transaction.md) | next: [242 row locks and table locks](./242-row-locks-and-table-locks.md)
