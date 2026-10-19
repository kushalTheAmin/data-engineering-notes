# 087: primary key, one unique id per row
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [082 a database, a program that guards your data](./082-a-database-guards-the-data.md)
section: tables, keys and relationships, part 9, ~2 min read

what if a second Chirag signs up? the name alone cant tell an order which Chirag it belongs to.

a primary key is a column (sometimes two together, a later note) in a [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid where each row is one record, like a spreadsheet) whose value is different in every row and never [NULL](./031-null.md) (no value), so one value points at exactly one row. in the shop, the imaginary gujarati snack store, the customers table uses customer_id. like the type rule in [080](./080-every-column-holds-one-type.md), the [database](./082-a-database-guards-the-data.md) (the program guarding the data) checks it every time a row is added. INSERT adds a row, and here a second Chirag tries to reuse id 3:

```sql
-- fails on purpose
INSERT INTO customers VALUES (3, 'Chirag', 'Edison', DATE '2026-06-01')
```

the database says duplicate key and refuses the row, so this lookup can match at most one row (SELECT reads rows back):

```sql
SELECT customer_id, name, city FROM customers WHERE customer_id = 3
```

```result
customer_id | name | city
3 | Chirag | Jersey City
```

WHERE name = 'Chirag' returns one row today but could someday return two, so the new Chirag gets id 6 and orders store the 6, not the name.

the gotcha i didnt expect: unique alone isnt enough. NULL means unknown, and SQL says you cant say one unknown equals another, so a column marked only UNIQUE can hold many NULL rows (DuckDB does). a primary key bans NULL too, or "the row with no id" would point at several rows. SQLite is the exception again, it allows NULL in most key columns. i expected the key to be some special extra, but its two rules on a column, unique and not NULL.

### check yourself

1. the orders table in the shop has order_id as its primary key and already holds order 101 for customer 1. someone inserts order 101 again, but for customer 2. accepted?
<details><summary>answer</summary>

refused. the key is the order_id column alone, so a different customer doesnt help. the tempting yes comes from thinking the whole row has to match.

</details>

2. someone inserts a customer with customer_id NULL. no existing id is NULL, so no clash. accepted?
<details><summary>answer</summary>

refused, a primary key cant be NULL. the no clash idea is the trap, the ban on NULL is a separate rule.

</details>

3. Asha and Chirag both live in Jersey City. what does WHERE city = 'Jersey City' return, and why isnt it a safe way to find Chirag?
<details><summary>answer</summary>

```sql
SELECT customer_id, name FROM customers WHERE city = 'Jersey City'
```

```result
customer_id | name
1 | Asha
3 | Chirag
```

two rows, because city isnt a key. WHERE customer_id = 3 gives at most one.

</details>

---
prev: [086 client and server, you ask, the database answers](./086-client-and-server.md) | next: [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md)
