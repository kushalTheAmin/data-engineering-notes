# 228: COMMIT and ROLLBACK, keeping or undoing a transaction
builds on: [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [093 foreign key](./093-foreign-key.md)
section: changing data safely, part 21, ~2 min read

i inserted an order, counted it, saw it sitting right there, typed one word and it was gone. no DELETE anywhere.

in [227](./227-transactions-all-or-nothing.md) a transaction was a group of changes that all happen or none do. you write one with three commands: BEGIN opens it, COMMIT keeps every change inside, ROLLBACK throws every change inside away. the shop, the imaginary gujarati snack store these notes run on, gets copies of its tables again (SQL run in DuckDB, a small database), my_items with a [foreign key](./093-foreign-key.md) (a column that must name a real row elsewhere):

```sql
CREATE TABLE my_orders AS SELECT * FROM orders;
CREATE TABLE my_items (order_id INTEGER, product_id INTEGER REFERENCES products (product_id), quantity INTEGER);
INSERT INTO my_items SELECT * FROM order_items
```

now Dishas order 108, two [INSERTs](./220-insert-adding-rows-and-matching-values-to-columns.md) (add a row each) inside a transaction, counted before i decide (count(*) counts rows, WHERE keeps the matching ones, UNION ALL stacks the two results):

```sql
BEGIN;
INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending');
INSERT INTO my_items VALUES (108, 1, 2);
SELECT 'my_orders' AS tbl, count(*) AS rows_for_108 FROM my_orders WHERE order_id = 108
UNION ALL SELECT 'my_items', count(*) FROM my_items WHERE order_id = 108
```

```result
tbl | rows_for_108
my_orders | 1
my_items | 1
```

nothing is final yet, but from inside the rows look normal. now i change my mind and count again:

```sql
ROLLBACK;
SELECT 'my_orders' AS tbl, count(*) AS rows_for_108 FROM my_orders WHERE order_id = 108
UNION ALL SELECT 'my_items', count(*) FROM my_items WHERE order_id = 108
```

```result
tbl | rows_for_108
my_orders | 0
my_items | 0
```

both gone together. same steps ending in COMMIT instead would leave both rows for good.

| command | what happens to the changes |
| --- | --- |
| COMMIT | all kept |
| ROLLBACK | all thrown away |

i figured a half done change would look half done from the inside, but my own count showed the finished picture right up to the rollback.

one gotcha: in DuckDB, when an insert inside breaks a foreign key, the whole transaction is dead and everything after is refused until it ends.

so what: Postgres docs say the updates of an open transaction are invisible to other connected users until it completes, then they all appear at once. and with no BEGIN, Postgres and DuckDB treat each statement as its own tiny transaction that commits by itself, which is why 227s order row stayed behind.

### check yourself

1. you run BEGIN, insert order 109 (Disha) and its item (dhokla, product 1), then COMMIT. then you type ROLLBACK to undo it. how many rows does 109 have in my_orders? count(*) counts rows.

```sql
BEGIN;
INSERT INTO my_orders VALUES (109, 4, TIMESTAMP '2026-04-10 12:00:00', 'pending');
INSERT INTO my_items VALUES (109, 1, 1);
COMMIT
```

```sql
-- fails on purpose
ROLLBACK
```

```sql
SELECT count(*) AS order_rows FROM my_orders WHERE order_id = 109
```

<details><summary>answer</summary>

```result
order_rows
1
```

COMMIT already made it permanent, so the ROLLBACK has nothing open to undo (DuckDB even errors). the tempting answer is 0, as if ROLLBACK could reach back past a COMMIT.

</details>

2. BEGIN, insert order 110 (Esha), then an item naming product 99, which doesnt exist, fails. you carry on: the good item (110, 1, 1) and COMMIT. does order 110 exist?

```sql
BEGIN;
INSERT INTO my_orders VALUES (110, 5, TIMESTAMP '2026-04-10 13:00:00', 'pending')
```

```sql
-- fails on purpose
INSERT INTO my_items VALUES (110, 99, 1)
```

```sql
-- fails on purpose
INSERT INTO my_items VALUES (110, 1, 1)
```

```sql
COMMIT;
SELECT count(*) AS order_rows FROM my_orders WHERE order_id = 110
```

<details><summary>answer</summary>

```result
order_rows
0
```

in DuckDB the foreign key failure aborts the whole transaction, so the good item is refused too and COMMIT ends it by rolling back. the tempting answer is 1, since the order insert itself worked.

</details>

---
prev: [227 transactions, all or nothing](./227-transactions-all-or-nothing.md) | next: [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md)
