# 223: DELETE, removing rows and what still points at them
builds on: [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [093 foreign key](./093-foreign-key.md), [094 what a foreign key stops, rows pointing at nothing](./094-what-a-foreign-key-stops.md), [031 null, a marker for a missing value](./031-null.md), [114 three valued logic, true, false and unknown](./114-three-valued-logic-true-false-and-unknown.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md)
section: changing data safely, part 16, ~2 min read

order 104 in the shop, the imaginary gujarati snack store these notes run on, is cancelled. so can you just delete it? i tried, and the database said no.

DELETE FROM removes the rows its [WHERE](./106-where-keeping-only-the-rows-that-match.md) picks, whole rows, where [UPDATE](./222-update-changing-rows-and-why-the-where-matters.md) changes one value. but other tables hold a [foreign key](./093-foreign-key.md) (a column pointing at another tables row) aimed at orders, and the database refuses to leave a pointer with nothing to point at, like in [094](./094-what-a-foreign-key-stops.md):

```sql
-- fails on purpose
DELETE FROM orders WHERE order_id = 104
```

so who is pointing at 104? in DuckDB (a database that runs inside your script), count(*) [counts rows](./138-count-star-vs-count-of-a-column.md) and UNION ALL stacks the three results, one per table:

```sql
SELECT 'order_items' AS tbl, count(*) AS rows_for_104 FROM order_items WHERE order_id = 104
UNION ALL SELECT 'order_fees', count(*) FROM order_fees WHERE order_id = 104
UNION ALL SELECT 'order_ratings', count(*) FROM order_ratings WHERE order_id = 104
```

```result
tbl | rows_for_104
order_items | 1
order_fees | 1
order_ratings | 0
```

two tables point at it, a line item and a 0.00 delivery fee. i expected one blocker and the database to tidy up behind the order, but there were two, and by default it never tidies on its own (Postgres can be told to, with ON DELETE CASCADE). those rows go first, the order last. a table nothing points at, like order_ratings, can be deleted from any time. leave the WHERE off and every row goes while the empty table stays, the same trap as [222](./222-update-changing-rows-and-why-the-where-matters.md).

so what: a deleted row is simply gone, and rows in other tables can disagree with it. thats a good reason the shop keeps 104 as a cancelled row, history stays.

### check yourself

1. orders 103 and 107 were never rated, so their stars are [NULL](./031-null.md) (a missing value). the five stars are 5, 4, NULL, 3, NULL. how many ratings remain after this?

```sql
DELETE FROM order_ratings WHERE stars < 4;
SELECT count(*) AS remaining FROM order_ratings
```

<details><summary>answer</summary>

```result
remaining
4
```

only the 3 is below 4. a test on NULL is [unknown](./114-three-valued-logic-true-false-and-unknown.md), and WHERE only acts on true, so those rows stay. the tempting answer is 2, reading NULL as small.

</details>

2. the shop sells 6 products. fafda is in no order, dhokla is in orders 101, 104 and 107. one of `DELETE FROM products WHERE name = 'fafda'` and the same for 'dhokla' errors. which, and what does the count return after the safe one?

```sql
DELETE FROM products WHERE name = 'fafda';
SELECT count(*) AS products FROM products
```

<details><summary>answer</summary>

```result
products
5
```

fafda goes, leaving 5. dhokla errors, since order_items still points at it. every row of products is in a table other tables point at, but only rows that something actually points at are protected.

</details>

---
prev: [222 UPDATE, changing rows and why the WHERE matters](./222-update-changing-rows-and-why-the-where-matters.md) | next: [224 upsert, insert or update in one statement](./224-upsert-insert-or-update-in-one-statement.md)
