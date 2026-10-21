# 137: aggregate functions, many rows in, one value out
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [101 SQL, you describe the result, the database figures out how](./101-sql-you-describe-the-result.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md), [136 capstone, one query traced clause by clause](./136-capstone-one-query-traced-clause-by-clause.md)
section: summarizing data, part 1, ~2 min read

how many items has the shop sold in total? every query in [136](./136-capstone-one-query-traced-clause-by-clause.md) gave back rows, but this answer is one number, so the rows have to collapse.

an aggregate function reads many rows and hands back one value. count(*) counts the rows, sum adds up a column, max finds the biggest. in python each is a loop with one running answer: a counter, a total, a best so far.

the queries below are [SQL](./101-sql-you-describe-the-result.md) (the language for asking a database for rows). the shop is the imaginary gujarati snack store these notes run on. its order_items [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) has 13 rows, one per product per order, each with a quantity:

```sql
SELECT count(*) AS rows_in, sum(quantity) AS total_qty, max(quantity) AS biggest FROM order_items
```

```result
rows_in | total_qty | biggest
13 | 20 | 3
```

13 rows went in and 1 came out. i figured an aggregate would add a column next to the 13 rows, but it replaces them, all three columns eat the same 13 rows and the originals are gone from the result.

[WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeping only matching rows) still runs first, so only the rows it keeps get aggregated. now a WHERE that keeps nothing, there is no order 999:

```sql
SELECT count(*) AS rows_in, sum(quantity) AS total_qty FROM order_items WHERE order_id = 999
```

```result
rows_in | total_qty
0 | NULL
```

counting nothing gives 0, but summing nothing gives a [null](./031-null.md) (a missing value), not 0. the docs of Postgres, a server database, say exactly this, except for count the everyday aggregates like sum and max return null when no rows are selected. a report for a day with no sales shows None unless you wrap it in [COALESCE](./116-coalesce-a-fallback-when-a-value-is-null.md) (a fallback for nulls).

---
prev: [136 capstone, one query traced clause by clause](./136-capstone-one-query-traced-clause-by-clause.md) | next: [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md)
