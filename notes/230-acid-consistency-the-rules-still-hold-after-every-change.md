# 230: ACID consistency, the rules still hold after every change
builds on: [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md), [228 COMMIT and ROLLBACK, keeping or undoing a transaction](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md), [227 transactions, all or nothing](./227-transactions-all-or-nothing.md), [217 CHECK, a rule every value must pass](./217-check-a-rule-every-value-must-pass.md)
section: changing data safely, part 23, ~2 min read

can a database let a transaction half break a rule, as long as it ends fine? and can it ever let a rule break that nobody told it about?

consistency, the C in [ACID](./229-acid-four-promises-a-database-makes.md) (four promises a database makes about changes), means every rule you declared is true before a transaction and true after it. the shop, the imaginary gujarati snack store these notes run on, gets a copy of products with a [CHECK](./217-check-a-rule-every-value-must-pass.md) (refuse a row whose test is false) that price must be above 0. one [transaction](./227-transactions-all-or-nothing.md) (changes that all happen or none do) tries two price changes:

```sql
CREATE TABLE my_products (product_id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, price DECIMAL(6, 2) CHECK (price > 0));
INSERT INTO my_products SELECT product_id, name, price FROM products;
BEGIN;
UPDATE my_products SET price = 7.00 WHERE name = 'dhokla'
```

```sql
-- fails on purpose
UPDATE my_products SET price = -1 WHERE name = 'kaju katli'
```

```sql
COMMIT;
SELECT name, price FROM my_products WHERE name IN ('dhokla', 'kaju katli') ORDER BY name
```

```result
name | price
dhokla | 6.00
kaju katli | 12.00
```

| step | the table | rules hold? |
| --- | --- | --- |
| before BEGIN | dhokla 6.00, kaju katli 12.00 | yes |
| dhokla to 7.00 | dhokla 7.00 | yes, mid way |
| kaju katli to -1 | refused | the whole transaction dies |
| after COMMIT | back to 6.00 and 12.00 | yes |

the good dhokla change vanished with the bad one. i expected only the bad row to be refused, but in DuckDB one refused change kills the whole transaction, so it takes back all of it (SQLite would keep the dhokla change, so this is a choice each database makes) ([228](./228-commit-and-rollback-keeping-or-undoing-a-transaction.md) showed DuckDB doing the same after a failed foreign key).

now the catch. a rule nobody declared isnt guarded. nothing says an order needs items, so order 108 goes in alone and every rule is happy. this query lists orders with no matching item row (LEFT JOIN keeps unmatched orders, with empty item columns):

```sql
CREATE TABLE my_orders AS SELECT * FROM orders;
CREATE TABLE my_items AS SELECT * FROM order_items;
INSERT INTO my_orders VALUES (108, 4, TIMESTAMP '2026-04-10 11:00:00', 'pending');
SELECT o.order_id FROM my_orders o LEFT JOIN my_items i ON i.order_id = o.order_id WHERE i.order_id IS NULL
```

```result
order_id
108
```

so what: a CHECK only sees the row being written, and the Postgres docs say it cant reference other rows, so rules like "every order has an item" live in app code or other tools. consistency is only as good as the rules you wrote down.

---
prev: [229 ACID, four promises a database makes](./229-acid-four-promises-a-database-makes.md) | next: [231 isolation, two people at the same time](./231-isolation-two-people-at-the-same-time.md)
