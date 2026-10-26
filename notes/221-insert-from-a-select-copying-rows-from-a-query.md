# 221: INSERT from a SELECT, copying rows from a query
builds on: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md), [213 CREATE TABLE, naming a table and its columns](./213-create-table-naming-a-table-and-its-columns.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [139 count distinct, counting different values](./139-count-distinct-counting-different-values.md), [218 key constraints, PRIMARY KEY and REFERENCES in CREATE TABLE](./218-key-constraints-primary-key-and-references-in-create-table.md)
section: changing data safely, part 14, ~2 min read

i copied the delivered orders into a new table, ran the copy twice, and got 10 rows when only 5 orders were ever delivered. no error, so where did the other 5 come from?

INSERT INTO a table followed by a SELECT adds whatever the query returns as new rows, instead of values you typed out like in [220](./220-insert-adding-rows-and-matching-values-to-columns.md). the shop, the imaginary gujarati snack store these notes run on, has 7 orders. i make an empty table with [CREATE TABLE](./213-create-table-naming-a-table-and-its-columns.md) (makes a table), then fill it from a [SELECT](./104-select-and-from-picking-columns.md) (picks columns) with a [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps only matching rows). in DuckDB, where ORDER BY sorts the rows:

```sql
CREATE TABLE delivered (order_id INTEGER, customer_id INTEGER, ordered_at TIMESTAMP);
INSERT INTO delivered SELECT order_id, customer_id, ordered_at FROM orders WHERE status = 'delivered';
SELECT * FROM delivered ORDER BY order_id
```

```result
order_id | customer_id | ordered_at
101 | 1 | 2026-04-01 09:15:00
102 | 2 | 2026-04-01 18:40:00
103 | 1 | 2026-04-03 12:05:00
105 | 4 | 2026-04-06 19:10:00
107 | 2 | 2026-04-09 13:45:00
```

i half expected a special copy command with its own rules, but the SELECT is exactly the one i already know, with INSERT in front. the 5 rows that come out (104 was cancelled, 106 pending) land matched by position, the same rule as 220, so swapping order_id and customer_id would go in silently.

now run the same INSERT again. count(*) counts all [rows](./138-count-star-vs-count-of-a-column.md), count(DISTINCT order_id) counts [different values](./139-count-distinct-counting-different-values.md):

```sql
INSERT INTO delivered SELECT order_id, customer_id, ordered_at FROM orders WHERE status = 'delivered';
SELECT count(*) AS total, count(DISTINCT order_id) AS different FROM delivered
```

```result
total | different
10 | 5
```

nothing remembers the first run, so every order is there twice. a [PRIMARY KEY](./218-key-constraints-primary-key-and-references-in-create-table.md) on order_id (a rule that no value repeats) would have refused the repeat.

so what: this shape fills one table from another, like a clean table from a raw one, and a loading job that retries copies the rows again unless the table refuses repeats. Postgres takes the same statement.

---
prev: [220 INSERT, adding rows and matching values to columns](./220-insert-adding-rows-and-matching-values-to-columns.md) | next: [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md)
