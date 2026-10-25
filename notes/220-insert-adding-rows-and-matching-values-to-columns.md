# 220: INSERT, adding rows and matching values to columns
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [080 every column holds one type](./080-every-column-holds-one-type.md), [031 null, a marker meaning there is no value](./031-null.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [215 NOT NULL and DEFAULT, required columns and fallback values](./215-not-null-and-default-required-columns-and-fallback-values.md)
section: changing data safely, part 13, ~2 min read

Chirag wants kaju katli (a cashew fudge sweet) on his wishlist, but the table says Disha saved jalebi (a fried, syrupy sweet). no error, so what happened?

INSERT INTO adds rows to a [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows and columns). the shop, the imaginary gujarati snack store these notes run on, gets a wishlist from [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (the command that makes a table). this runs in DuckDB, a small database with no server (ORDER BY sorts the rows):

```sql
CREATE TABLE wishlist (customer_id INTEGER, product_id INTEGER, added_on DATE);
INSERT INTO wishlist VALUES (1, 1, '2026-04-01'), (2, 3, '2026-04-02');
INSERT INTO wishlist (product_id, customer_id) VALUES (1, 5);
INSERT INTO wishlist VALUES (4, 3, '2026-04-03');
SELECT * FROM wishlist ORDER BY customer_id
```

```result
customer_id | product_id | added_on
1 | 1 | 2026-04-01
2 | 3 | 2026-04-02
4 | 3 | 2026-04-03
5 | 1 | NULL
```

the first insert has no column list (names in brackets after the table), so values go to columns by position. the second names its columns, so 1 is the product and 5 the customer, and the left out added_on becomes [NULL](./031-null.md) (no value), since it has no [DEFAULT](./215-not-null-and-default-required-columns-and-fallback-values.md) (a fallback for left out columns). the third is the bug: i meant customer 3, product 4, but typed product first. both are whole numbers, so Disha (4) got jalebi (3).

you know this from a function call with two swapped numbers, even typescript (typed javascript) cant tell. i expected the database to catch it, but it only checks the rules on the table, like each [column type](./080-every-column-holds-one-type.md) (the kind of value allowed), never what you meant.

```sql
-- fails on purpose
INSERT INTO wishlist VALUES (5, 2)
```

DuckDB refuses a count that doesnt match. Postgres, a popular server database, is looser: its docs say with no column list and too few values, the rest take their default or NULL. so i name the columns, and a mix up shows in the line.

---
prev: [219 sequences, where made up ids come from](./219-sequences-where-made-up-ids-come-from.md) | next: not written yet
