# 236: dirty reads
builds on: [235 lost updates](./235-lost-updates.md), [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
section: changing data safely, part 29, ~2 min read

Esha types 60.00 instead of 6.00 for dhokla, spots the typo a second later and rolls it back. if Asha looked in that second, what price did she see?

[235](./235-lost-updates.md) was two writers stepping on each other, now a reader gets hurt. a dirty read is reading a change from a [transaction](./227-transactions-all-or-nothing.md) (a group of changes that all happen or none do) that hasnt [committed](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) (made permanent) yet. here is the shop, the imaginary gujarati snack store these notes run on, on a database that allows it:

| step | Esha | Asha reads dhokla | committed price |
|---|---|---|---|
| 1 | BEGIN (open a transaction), UPDATE price to 60.00 | | 6.00 |
| 2 | | 60.00 (dirty read) | 6.00 |
| 3 | ROLLBACK | | 6.00 |
| 4 | | 6.00 | 6.00 |

the last column never moves, the committed price is 6.00 the whole time. this reads one row of the products table:

```sql
SELECT name, price FROM products WHERE name = 'dhokla'
```

```result
name | price
dhokla | 6.00
```

at step 2 Asha read a draft. at step 3 the draft was thrown away, so her 60.00 now comes from nowhere. if she showed it to a customer or saved it into a report, that copy outlives the rollback. i assumed a dirty read needed a bug or a crash, but it only needs a read at the wrong second.

[isolation](./231-isolation-two-people-at-the-same-time.md) (simultaneous users dont see half done work) is the promise that stops this, and its why Asha counted 7 orders while order 108 was unfinished. the weakest isolation level in the SQL standard, read uncommitted, is where dirty reads are allowed. Postgres, a database that runs as its own server, accepts that level but the docs say it behaves like read committed there, so it never shows you one.

### check yourself

1. a dashboard runs on a database that allows dirty reads. Esha has inserted order 108 but not committed, and the dashboard counts orders, then she rolls back. what did it show, and what is the true count?

```sql
SELECT count(*) AS orders_now FROM orders
```

<details><summary>answer</summary>

```result
orders_now
7
```

the dashboard showed 8 and the true count is 7. the tempting 7 is what an isolated database would show, but this one let the draft through.

</details>

2. Esha commits the typo 60.00, Asha reads 60.00, then Esha commits a second UPDATE back to 6.00. was the read of Asha dirty?

<details><summary>answer</summary>

no. the 60.00 was committed when she read it, so it was a real price for a while, just a wrong one. dirty means uncommitted. yes is tempting because the number turned out wrong, but wrong and dirty are different things.

</details>

---
prev: [235 lost updates](./235-lost-updates.md) | next: not written yet
