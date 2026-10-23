# 180: CTEs, naming each step with WITH
builds on: [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [175 subquery in FROM](./175-subquery-in-from.md), [176 scalar subqueries, one value inside a query](./176-scalar-subqueries-one-value-inside-a-query.md)
section: bigger queries, part 7, ~2 min read

have you noticed a query with another query nested inside it makes you start in the middle? i kept hunting for the innermost parentheses and working outward. there is a way to read it top to bottom.

a CTE (common table expression) gives an inner query a name up front with WITH, and the main query then uses that name like a table. it is a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT the outer query reads as a table), written top to bottom. the shop, the imaginary gujarati snack store these notes run on, has an orders table of 7 rows (order_id, customer_id, status like delivered or cancelled). here is the query from 175 again, [GROUP BY](./143-group-by-one-group-per-value.md) counting orders per customer:

```sql
WITH per_customer AS (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) SELECT avg(orders) AS avg_orders FROM per_customer
```

```result
avg_orders
1.75
```

same 1.75. the inner query just moved to the top and got a name, like `per_customer = ...` in python, except the name only lives for this one statement.

the payoff is using the name twice. here per_customer is read as a table, and again inside a [scalar subquery](./176-scalar-subqueries-one-value-inside-a-query.md) (one value in parentheses) to keep customers above that 1.75 average. the [inner join](./156-inner-join-traced-by-hand.md) (pairs rows where ids match) fetches names, and [p and c](./158-table-aliases-short-nicknames-for-tables.md) are nicknames:

```sql
WITH per_customer AS (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) SELECT c.name, p.orders FROM per_customer p JOIN customers c ON c.customer_id = p.customer_id WHERE p.orders > (SELECT avg(orders) FROM per_customer) ORDER BY c.name
```

```result
name | orders
Asha | 3
Bhavin | 2
```

i assumed WITH was a new feature, but it is the same inner query with a label. Postgres (a server database) says it can be thought of as a temporary table that exists just for one query. the label can even reuse a real tables name, and for the rest of the statement it wins.

### check yourself

1. predict n. the inner orders is the real table, the outer one is the CTE.
```sql
WITH orders AS (SELECT * FROM orders WHERE status = 'delivered') SELECT count(*) AS n FROM orders
```
<details><summary>answer</summary>

```result
n
5
```
the outer orders is the CTE, which holds the 5 delivered orders. the tempting answer is 7, from thinking the real table still wins.

</details>

2. this CTE is never used. predict n.
```sql
WITH delivered AS (SELECT * FROM orders WHERE status = 'delivered') SELECT count(*) AS n FROM orders
```
<details><summary>answer</summary>

```result
n
7
```
the main query reads orders, the real table, so all 7 rows count. a name only filters when you actually put it in FROM. the tempting answer is 5.

</details>

---
prev: [179 NOT IN and the NULL trap](./179-not-in-and-the-null-trap.md) | next: [181 views, a saved query with a name](./181-views-a-saved-query-with-a-name.md)
