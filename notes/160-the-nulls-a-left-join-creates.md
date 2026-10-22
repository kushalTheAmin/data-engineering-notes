# 160: the nulls a left join creates
builds on: [031 null, a marker for a missing value](./031-null.md), [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md)
section: combining tables with joins, part 6, ~2 min read

how many orders did Esha place? ask a left join with count(*) and it says 1. she has never ordered anything.

in [159](./159-left-join-keep-every-row-from-the-left-table.md) a left join (keeps every row of the first table, matched or not) kept Esha with order_id [NULL](./031-null.md) (a missing value). that NULL is made by the join, it isnt stored anywhere. order_id is the primary key of orders (a column that is unique and never NULL), and it still shows up NULL in the result, because the row was filled in for the missing partner. [grouping](./143-group-by-one-group-per-value.md) (one row per customer) on the shop (the imaginary gujarati snack store these notes run on), with [aliases](./158-table-aliases-short-nicknames-for-tables.md) c and o:

```sql
SELECT c.name, count(*) AS rows_kept, count(o.order_id) AS orders FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name ORDER BY c.name
```

```result
name | rows_kept | orders
Asha | 3 | 3
Bhavin | 2 | 2
Chirag | 1 | 1
Disha | 1 | 1
Esha | 1 | 0
```

only the last row disagrees. [count(*)](./138-count-star-vs-count-of-a-column.md) counts rows, and Esha has one, the filled-in one. count(o.order_id) skips NULL, so her group of one row counts 0. i trusted count(*) because it never skips anything, and thats exactly why it bites here.

so after a left join, count a column from the right table, one that is never NULL in the real table, like its primary key. count(*) answers "how many rows", and you wanted "how many orders".

---
prev: [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md) | next: not written yet
