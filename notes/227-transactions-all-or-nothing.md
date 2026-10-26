# 227: transactions, all or nothing
builds on: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [093 foreign key](./093-foreign-key.md), [219 sequences, where made up ids come from](./219-sequences-where-made-up-ids-come-from.md)
section: changing data safely, part 20, ~2 min read

placing an order in the shop, the imaginary gujarati snack store these notes run on, is two inserts: a row in orders, then a row in order_items. what if the second one fails after the first one worked?

a transaction is a group of changes the database treats as one, so either every change in it happens or none does. i only waved at the word in [219](./219-sequences-where-made-up-ids-come-from.md), here is why it exists. first the world without one, on copies so the real tables stay put. my_items has a [foreign key](./093-foreign-key.md) (a column pointing at another tables row) to products, and Disha places order 108:

```sql
CREATE TABLE my_orders AS SELECT * FROM orders;
CREATE TABLE my_items (order_id INTEGER, product_id INTEGER REFERENCES products (product_id), quantity INTEGER);
INSERT INTO my_items SELECT * FROM order_items;
INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending')
```

step 2 names product 99, which doesnt exist:

```sql
-- fails on purpose
INSERT INTO my_items VALUES (108, 99, 1)
```

so what does the shop hold now? UNION ALL stacks the two counts, one per table:

```sql
SELECT 'my_orders' AS tbl, count(*) AS rows_for_108 FROM my_orders WHERE order_id = 108
UNION ALL SELECT 'my_items', count(*) FROM my_items WHERE order_id = 108
```

```result
tbl | rows_for_108
my_orders | 1
my_items | 0
```

| | order row 108 | item row for 108 |
| --- | --- | --- |
| no transaction | stays | none |
| inside a transaction | undone too | none |

an order with nothing in it. i expected the failed step to cancel the whole script, but the database judges each statement alone and never reaches back. wrap both steps in a transaction and step 1 is undone as well, as if it never happened. one statement on its own is already all or nothing, even an [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md) over many rows.

so what: the Postgres docs open with a bank payment, money out of Alice, money into Bob, and a crash between the two would make money vanish. how you actually write a transaction is for a later note.

### check yourself

1. no transaction anywhere. Disha places order 109 with a good item (dhokla, product 1) and then a bad one (product 99). how many item rows does 109 have afterwards?

```sql
-- fails on purpose
INSERT INTO my_orders VALUES (109, 4, TIMESTAMP '2026-04-10 12:00:00', 'pending');
INSERT INTO my_items VALUES (109, 1, 1);
INSERT INTO my_items VALUES (109, 99, 1)
```

```sql
SELECT count(*) AS item_rows FROM my_items WHERE order_id = 109
```

<details><summary>answer</summary>

```result
item_rows
1
```

the dhokla row went in before the failure and nothing undoes it. the tempting answer is 0, reading a failure as cancelling the whole script.

</details>

2. order 102 has products 3 and 4. one UPDATE adds 3 to every product_id there, so 3 becomes 6 (real) and 4 becomes 7 (no such product), and it errors. which products does 102 hold after?

```sql
-- fails on purpose
UPDATE my_items SET product_id = product_id + 3 WHERE order_id = 102
```

```sql
SELECT product_id FROM my_items WHERE order_id = 102 ORDER BY product_id
```

<details><summary>answer</summary>

```result
product_id
3
4
```

one statement is all or nothing, so the row that could have moved to 6 stayed put. the tempting answer is 4 and 6, thinking the good row went through.

</details>

---
prev: [226 DROP and TRUNCATE, emptying a table vs removing it](./226-drop-and-truncate-emptying-a-table-vs-removing-it.md) | next: [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md)
