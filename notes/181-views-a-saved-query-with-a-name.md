# 181: views, a saved query with a name
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [180 CTEs, naming each step with WITH](./180-ctes-naming-each-step-with-with.md)
section: bigger queries, part 8, ~2 min read

you save a query under a name, the shop gets a new order, and the saved thing now shows a different answer. i would have bet it was a stored copy of the rows. is it?

a view is a query saved in the database under a name, and you read it like a table. a [CTE](./180-ctes-naming-each-step-with-with.md) (a named inner query, alive for one statement) is the same idea, except a view stays until you drop it. the shop, the imaginary gujarati snack store these notes run on, has 7 orders, 5 of them delivered. save that [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps rows passing a test), then [count](./138-count-star-vs-count-of-a-column.md) the view:

```sql
CREATE VIEW delivered_orders AS SELECT * FROM orders WHERE status = 'delivered'; SELECT count(*) AS n FROM delivered_orders
```

```result
n
5
```

now pretend order 106, Ashas pending one, just got delivered. UPDATE changes values in rows that already exist. i touch only the orders table and ask the same view again:

```sql
UPDATE orders SET status = 'delivered' WHERE order_id = 106; SELECT count(*) AS n FROM delivered_orders
```

```result
n
6
```

5 became 6 and i never touched the view. it never held rows, only the query, which runs again each time something reads it. in python it is a function you call, not a list you saved: `delivered_orders = lambda: [o for o in orders if o["status"] == "delivered"]`.

so a view is always fresh and costs no storage, but you pay for the work on every read. a view that stores its answer instead is called a materialized view, and Postgres (a server database) has both. this is how teams give analysts a clean `delivered_orders` and keep the messy filter in one place.

### check yourself

1. the view above counts 6 now. order 107 then gets cancelled. predict n.
```sql
UPDATE orders SET status = 'cancelled' WHERE order_id = 107; SELECT count(*) AS n FROM delivered_orders
```
<details><summary>answer</summary>

```result
n
5
```
the view reruns on the current orders, where 107 no longer passes. the tempting answer is 6, from picturing saved rows.

</details>

2. a view cheap is saved, then dhokla (price 6.00) drops to 5.00. predict the count before and after.
```sql
CREATE VIEW cheap AS SELECT * FROM products WHERE price < 6; SELECT count(*) AS n FROM cheap
```
```result
n
3
```
```sql
UPDATE products SET price = 5.00 WHERE name = 'dhokla'; SELECT count(*) AS n FROM cheap
```
<details><summary>answer</summary>

```result
n
4
```
dhokla now passes price < 6, and the view picked it up with no change to itself. the tempting answer is 3.

</details>

---
prev: [180 CTEs, naming each step with WITH](./180-ctes-naming-each-step-with-with.md) | next: [182 UNION and UNION ALL](./182-union-and-union-all.md)
