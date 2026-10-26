# 229: ACID, four promises a database makes
builds on: [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [217 CHECK, a rule every value must pass](./217-check-a-rule-every-value-must-pass.md), [036 memory vs disk](./036-memory-vs-disk.md)
section: changing data safely, part 22, ~2 min read

a power cut mid order, two shoppers at once, a price of -5, a crash right after saving. four ways to wreck the orders of the shop, the imaginary gujarati snack store these notes run on, and a database has a named promise against each one.

ACID is the name for those four promises, one letter each. they cover a [transaction](./227-transactions-all-or-nothing.md), a group of changes that all happen or none do:

| letter | the promise | what breaking it looks like |
| --- | --- | --- |
| A, atomicity | all of a transaction happens, or none of it | order 108 saved, its items missing |
| C, consistency | the rules still hold after every change | a product priced -5 gets in |
| I, isolation | people working at once dont see each others half done work | Asha counts orders mid way through Dishas, sees one that later vanishes |
| D, durability | once COMMIT (keep the changes) says done, a crash cant undo it | Esha is told her order is saved, the power dies, it is gone |

A is [227](./227-transactions-all-or-nothing.md), and [COMMIT and ROLLBACK](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) are how you ask for it. C leans on rules like [CHECK](./217-check-a-rule-every-value-must-pass.md) (refuse a row whose test is false), but only rules somebody wrote down: a price of 600.00 sails through CHECK (price > 0). D means the changes reach the [disk](./036-memory-vs-disk.md), storage that keeps bytes without power, before the database says done, with default settings.

i kept hearing ACID as one big safety label, but its four separate promises, and a crash can break one and leave the others alone. a power cut before COMMIT is an A question, after COMMIT its a D question.

so what: Postgres, a popular server database, describes atomic and durable in these terms in its docs. isolation is the slippery one, since you choose how strict it is, and Postgres by default is not at the strictest level, so some oddities can still slip through. each letter gets its own note.

### check yourself

1. the shop inserts order 108, then loses power before the items go in or COMMIT runs. after restart the order row exists with no items. which promise broke, A or D?

<details><summary>answer</summary>

A. nothing was committed, so the whole transaction should have vanished. D is tempting because of the crash, but D covers only work COMMIT confirmed.

</details>

2. products has 6 rows. this copy of it has CHECK (price > 0), and someone inserts imarti at -5.00. predict count(*), the number of rows, afterwards. which letter did the refusing?

```sql
CREATE TABLE my_products (product_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0));
INSERT INTO my_products SELECT product_id, name, price FROM products
```

```sql
-- fails on purpose
INSERT INTO my_products VALUES (7, 'imarti', -5.00)
```

```sql
SELECT count(*) AS products FROM my_products
```

<details><summary>answer</summary>

```result
products
6
```

C, a rule said no. the tempting answer is 7, picturing the insert going in anyway.

</details>

3. imagine a database that lets this happen: Esha places an order, Asha counts all orders and sees 8, then Esha rolls back and a recount shows 7. which promise did it fail to keep? (Postgres doesnt.)

<details><summary>answer</summary>

isolation. Asha saw work that was never final. the tempting answer is A, but Eshas rollback was clean, the problem is who got to look in the middle.

</details>

---
prev: [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) | next: [230 ACID consistency, the rules still hold after every change](./230-acid-consistency-the-rules-still-hold-after-every-change.md)
