# 167: anti join, rows with no match
builds on: [031 null, a marker for a missing value](./031-null.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md), [161 a WHERE that quietly turns a left join into an inner join](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md)
section: combining tables with joins, part 13, ~2 min read

which customers have never ordered anything? an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) cant tell you, because the people you want are exactly the rows it throws away.

an anti join keeps the rows of one table that have no match in the other. you already own the parts, a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every row of the table written first) fills the missing partner with [NULL](./031-null.md) (a missing value), so you keep only the rows where that happened. the shop, the imaginary gujarati snack store these notes run on:

```sql
SELECT c.name, o.order_id FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL
```

```result
name | order_id
Esha | NULL
```

the join makes 8 rows and only Eshas order_id is NULL, so [IS NULL](./115-is-null-and-is-not-null.md) (true when a value is missing) keeps her. its the `if not found` from 159, printing only the unmatched ones.

the column you test matters. use the right tables primary key (its unique id), like order_id, because in [160](./160-the-nulls-a-left-join-creates.md) that column is never NULL in a real row, so a NULL there can only mean no match. test a column that can be NULL in real rows and people who did order sneak in.

same shape, other table: which products never appear in an order?

```sql
SELECT p.name FROM products p LEFT JOIN order_items i ON p.product_id = i.product_id WHERE i.product_id IS NULL
```

```result
name
fafda
```

fafda, a crunchy fried snack, has never been ordered. i assumed finding what is missing needed its own kind of join, and its the same left join with one filter. [161](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md) warned that a right side test in WHERE kills the NULLs, and IS NULL is the one test that goes looking for them.

its the query behind who never bought.

### check yourself

1. Chirag has one order, but it was cancelled. you want customers with no delivered order. what does this return?

```sql
SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' WHERE o.order_id IS NULL ORDER BY c.name
```

<details><summary>answer</summary>

```result
name
Chirag
Esha
```

the status test sits in the ON, so Chirags cancelled order is not a match and he gets the filled in NULL like Esha. the tempting answer is just Esha, from thinking anyone with an order row is safe.

</details>

2. a teammate flips the tables, `orders o LEFT JOIN customers c`, and keeps `WHERE c.customer_id IS NULL`. how many rows come back, and why?

```sql
SELECT count(*) AS n FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id WHERE c.customer_id IS NULL
```

<details><summary>answer</summary>

```result
n
0
```

now the left table is orders, and every order has a customer, so nothing is unmatched. an anti join answers "which left rows have no partner", so the table you want the missing ones from must be written first. the tempting answer is 1, from expecting Esha to show up whichever way round.

</details>

---
prev: [166 joining on columns that can be NULL](./166-joining-on-columns-that-can-be-null.md) | next: not written yet
