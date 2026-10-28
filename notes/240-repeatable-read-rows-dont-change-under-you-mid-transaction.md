# 240: repeatable read, rows dont change under you mid transaction
builds on: [239 isolation levels, read committed](./239-isolation-levels-read-committed.md), [238 phantoms](./238-phantoms.md), [237 non repeatable reads](./237-non-repeatable-reads.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
section: changing data safely, part 33, ~2 min read

Esha commits order 108 in the middle of Ashas transaction, but this time Asha counts the orders twice and gets the same number both times. same script as last note, so what did i change?

one setting. repeatable read is an [isolation level](./239-isolation-levels-read-committed.md) (how much of others work a transaction sees) where, in Postgres (a database that runs as its own server), the picture, a frozen view of the data, is taken once and kept until the [transaction](./227-transactions-all-or-nothing.md) ends. the name is looser elsewhere, SQL Server still lets new rows in. you ask for it like this:

```text
-- Postgres
BEGIN ISOLATION LEVEL REPEATABLE READ;
```

here it is next to [read committed](./239-isolation-levels-read-committed.md) (each query gets a fresh picture). the shop, the imaginary gujarati snack store these notes run on, has 7 orders, and 108 is imagined:

| step | who does | read committed | repeatable read |
|---|---|---|---|
| 1 | asha BEGIN | - | - |
| 2 | asha counts orders | 7 | 7 |
| 3 | esha INSERT 108, COMMIT | - | - |
| 4 | asha counts orders | 8 | 7 |
| 5 | asha [COMMIT](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (make it permanent) | - | - |
| 6 | asha counts orders, new transaction | 8 | 8 |

a [non repeatable read](./237-non-repeatable-reads.md) (one row, two values) and a [phantom](./238-phantoms.md) (a different set of rows) both need the second look to differ, so neither can happen here. the Postgres docs say this beats what the SQL standard (the official written rules for SQL) asks for here.

the catch: the picture starts at the first query, not BEGIN, so a commit between them still shows up. being out of date is the feature: Asha knows 108 exists and still gets 7.

so what: a report of five queries now adds up. the price, per the docs, is that if Asha tries to change a row Esha already changed, Postgres refuses with an error and the app must retry the transaction.

### check yourself

1. at repeatable read, Asha counts pending orders as her first query. then Esha commits order 106 as delivered, an imagined change. Asha counts again. what are her two numbers?

```sql
SELECT count(*) AS pending_now FROM orders WHERE status = 'pending'
```

<details><summary>answer</summary>

```result
pending_now
1
```

she gets 1 both times. the tempting 1 then 0 reads the second query as a fresh look, but her picture was taken at the first query and holds.

</details>

2. the shop has one pending order, 106. at repeatable read, Asha does BEGIN and nothing else. Esha commits a pending order 108, imagined. only then does Asha run her first query, counting pending orders. what does she get?

<details><summary>answer</summary>

2, the real pending order 106 plus 108. the picture starts at her first query, so the commit before it is inside. the tempting 1 assumes BEGIN took the picture.

</details>

---
prev: [239 isolation levels, read committed](./239-isolation-levels-read-committed.md) | next: [241 serializable, as if one at a time, and retrying the failures](./241-serializable-as-if-one-at-a-time-and-retrying-the-failures.md)
