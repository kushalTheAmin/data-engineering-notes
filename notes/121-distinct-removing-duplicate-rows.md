# 121: DISTINCT, removing duplicate rows
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [104 SELECT and FROM, picking columns](./104-select-and-from-picking-columns.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md)
section: asking questions with SQL, part 21, ~2 min read

in [104](./104-select-and-from-picking-columns.md) a plain SELECT category (a SQL query, a request to a database) gave me snack three times and i left it there. the fix is one word.

DISTINCT goes right after SELECT and keeps one copy of each different row in the result. think of a python loop with a seen list, a row only goes out the first time you meet it, and the order out isnt promised. here it is on the products [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows) of the shop, the imaginary gujarati snack store these notes run on:

```sql
SELECT DISTINCT category FROM products ORDER BY category
```

```result
category
drink
snack
sweet
```

the 6 category values were snack, snack, sweet, sweet, drink, snack, so six rows became three. now the part i got wrong, on the orders table, customer and status, first as is and then with DISTINCT:

```sql
SELECT customer_id, status FROM orders ORDER BY customer_id, status
```

```result
customer_id | status
1 | delivered
1 | delivered
1 | pending
2 | delivered
2 | delivered
3 | cancelled
4 | delivered
```

```sql
SELECT DISTINCT customer_id, status FROM orders ORDER BY customer_id, status
```

```result
customer_id | status
1 | delivered
1 | pending
2 | delivered
3 | cancelled
4 | delivered
```

7 rows became 5, even though only 4 customers ordered. i read DISTINCT as belonging to the first column after it, and it covers the whole row. customer 1 stays twice because delivered and pending are different pairs, only a pair that repeats collapses.

one edge: a test against a missing value is unknown, neither true nor false ([114](./114-three-valued-logic-true-false-and-unknown.md)), yet in DuckDB (the database these notes run in) two [nulls](./031-null.md) in a DISTINCT collapse into one.

i sorted with [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (sorting the result) on purpose. the docs of Postgres, a server database, say without it rows come back in whatever order is fastest, and DISTINCT doesnt change that. counting the distinct values is a later note.

---
prev: [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md) | next: [122 computed columns and AS](./122-computed-columns-and-as.md)
