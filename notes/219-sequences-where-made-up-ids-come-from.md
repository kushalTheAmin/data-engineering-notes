# 219: sequences, where made up ids come from
builds on: [088 natural keys vs made up ids](./088-natural-keys-vs-made-up-ids.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md), [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md)
section: changing data safely, part 12, ~2 min read

Asha gets support ticket 1, Bhavin gets 2, then one insert fails, and Chirag gets ticket 4. where did 3 go?

a sequence is a counter the database keeps on its own, outside any table. nextval is the call that hands out the next number and moves the counter on, for good. put it in a [DEFAULT](./215-not-null-and-default-required-columns-and-fallback-values.md) (the value used when an insert leaves a column out) and the database fills a [made up id](./088-natural-keys-vs-made-up-ids.md) (a meaningless number it hands out) for you. the shop, the imaginary gujarati snack store these notes run on, gets a tickets table, in DuckDB:

```sql
CREATE SEQUENCE ticket_id START 1;
CREATE TABLE tickets (ticket_id INTEGER PRIMARY KEY DEFAULT nextval('ticket_id'), customer VARCHAR NOT NULL);
INSERT INTO tickets (customer) VALUES ('Asha'), ('Bhavin')
```

a [PRIMARY KEY](./218-key-constraints-primary-key-and-references-in-create-table.md) is the unique, never missing id column. now one insert with no customer, which [NOT NULL](./215-not-null-and-default-required-columns-and-fallback-values.md) (refuse a missing value) refuses, then Chirag:

```sql
-- fails on purpose
INSERT INTO tickets (customer) VALUES (NULL)
```

```sql
INSERT INTO tickets (customer) VALUES ('Chirag');
SELECT * FROM tickets ORDER BY ticket_id
```

```result
ticket_id | customer
1 | Asha
2 | Bhavin
4 | Chirag
```

| step | counter hands out | table keeps |
| --- | --- | --- |
| Asha | 1 | 1 |
| Bhavin | 2 | 2 |
| no customer | 3 | nothing, row refused |
| Chirag | 4 | 4 |

in DuckDB the id was taken before the row got refused, and a counter never steps back, even if a transaction (a group of changes that can be undone together) rolls back. i assumed ids would count up with no holes, but a number once handed out stays used. thats fine, an id only has to be unique, not tidy.

Postgres, a popular server database, has the same gaps, and its docs say a sequence cant give gapless numbers. its serial columns are a sequence plus a DEFAULT nextval underneath, and some other databases call the same idea AUTO_INCREMENT. so never read a missing id as a deleted row, and dont use one as an invoice count.

### check yourself

1. Chirags ticket 4 is deleted, then Disha opens one. which id does she get?
```sql
DELETE FROM tickets WHERE customer = 'Chirag';
INSERT INTO tickets (customer) VALUES ('Disha');
SELECT ticket_id FROM tickets WHERE customer = 'Disha'
```
<details><summary>answer</summary>

```result
ticket_id
5
```
she gets 5. the counter lives outside the table and only moves forward, so 4 is not reused. the tempting answer is 4, because it looks free.

</details>

2. a small orders table is loaded with ids 101 and 102 typed by hand, and then one new order is added without an id. what id does it get?
```sql
CREATE SEQUENCE o START 1;
CREATE TABLE orders2 (order_id INTEGER PRIMARY KEY DEFAULT nextval('o'), status VARCHAR);
INSERT INTO orders2 VALUES (101, 'delivered'), (102, 'delivered');
INSERT INTO orders2 (status) VALUES ('pending');
SELECT order_id FROM orders2 WHERE status = 'pending'
```
<details><summary>answer</summary>

```result
order_id
1
```
it gets 1. the sequence never looks at the table, so typed ids dont move it. the clash waits until the counter reaches 101. the tempting answer is 103, which is what some other databases pick.

</details>

---
prev: [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md) | next: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md)
