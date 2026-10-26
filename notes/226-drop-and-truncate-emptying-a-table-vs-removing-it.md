# 226: DROP and TRUNCATE, emptying a table vs removing it
builds on: [225 ALTER TABLE, adding a column to a table that already has rows](./225-alter-table-adding-a-column-to-a-table-with-rows.md), [223 DELETE, removing rows and what still points at them](./223-delete-removing-rows-and-what-still-points-at-them.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [093 foreign key](./093-foreign-key.md)
section: changing data safely, part 19, ~2 min read

after [DELETE](./223-delete-removing-rows-and-what-still-points-at-them.md) with no WHERE the table is empty, so why does SQL have two more ways to get rid of data?

they go different distances. TRUNCATE removes every row and keeps the table. DROP TABLE removes the table itself, rows and column list together. the shop, the imaginary gujarati snack store these notes run on, gets its menu copy back (the three products under 6, a slice: fafda, jalebi, masala chai), in DuckDB:

| command | rows | table |
| --- | --- | --- |
| DELETE FROM menu | gone | stays |
| TRUNCATE menu | gone | stays |
| DROP TABLE menu | gone | gone |

```sql
CREATE TABLE menu AS SELECT name, price FROM products WHERE price < 6;
TRUNCATE menu;
INSERT INTO menu VALUES ('imarti', 6.00);
SELECT * FROM menu
```

```result
name | price
imarti | 6.00
```

the 3 old rows are gone but the columns survived, so the next INSERT just works. DROP TABLE goes further, it un-does the [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) itself:

```sql
-- fails on purpose
DROP TABLE menu;
SELECT * FROM menu
```

the table is not empty, it doesnt exist, so the error is about the name.

i kept assuming TRUNCATE was just a shouty DELETE. the Postgres docs say it gives the same result as a DELETE with no WHERE but doesnt scan the rows, so its faster and frees disk space right away. the catch, per the same docs, is that Postgres refuses to drop, or truncate on its own, a table another table points at with a [foreign key](./093-foreign-key.md) (a column pointing at another tables row), unless you add CASCADE (truncate can instead list both tables in one command), and you should read that word twice before typing it.

---
prev: [225 ALTER TABLE, adding a column to a table with rows](./225-alter-table-adding-a-column-to-a-table-with-rows.md) | next: [227 transactions, all or nothing](./227-transactions-all-or-nothing.md)
