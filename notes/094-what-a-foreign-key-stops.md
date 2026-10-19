# 094: what a foreign key stops, rows pointing at nothing
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md), [092 relationships, one customer, many orders](./092-relationships-one-customer-many-orders.md), [093 foreign key](./093-foreign-key.md)
section: tables, keys and relationships, part 16, ~2 min read

can you add an order for customer 9 when the shop, the imaginary gujarati snack store, only has 5 customers? the database says no, and thats the whole job of a foreign key.

once a [foreign key](./093-foreign-key.md) (a column holding another tables primary key values) is declared, the [database](./082-a-database-guards-the-data.md) (the program guarding the data) refuses any row whose pointer matches nothing. a row like that is an orphan row. here is the insert, with a customer_id that doesnt exist:

```sql
-- fails on purpose
INSERT INTO orders VALUES (108, 9, TIMESTAMP '2026-04-10 10:00:00', 'new')
```

DuckDB, the database these notes run, answers that key customer_id 9 does not exist in the referenced table. now the other direction. Chirag has order 104, so deleting him would leave 104 pointing at nothing:

```sql
-- fails on purpose
DELETE FROM customers WHERE customer_id = 3
```

refused too, the error says the key is still referenced. Esha has the empty pile from [092](./092-relationships-one-customer-many-orders.md), so nothing points at her:

```sql
SELECT count(*) AS esha_orders FROM orders WHERE customer_id = 5
```

```result
esha_orders
0
```

so deleting her would go through. i assumed the guard only watched new rows, but it also protects the row being pointed at. the rule is one sentence, every pointer that holds a value must match a real row, at all times.

Postgres lets you pick what a delete does, and ON DELETE CASCADE deletes the pointing rows along with it. handy for order items inside an order, scary for most else.

the shop file already uses one more trick on order_items, a key made of two columns, and a later note takes that apart.

---
prev: [093 foreign key](./093-foreign-key.md) | next: [095 composite keys](./095-composite-keys.md)
