# 175: subquery in FROM
builds on: [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [174 subquery in WHERE](./174-subquery-in-where.md)
section: bigger queries, part 2, ~2 min read

what is the average number of orders per customer? i tried avg(count(*)) and the database just said no. have you hit this one?

```sql
-- fails on purpose
SELECT avg(count(*)) FROM orders GROUP BY customer_id
```

an aggregate cant sit inside another aggregate in DuckDB or Postgres. a subquery in FROM fixes that: the inner SELECT sits in parentheses where a table name would go, and the outer query reads its result like a table. [174](./174-subquery-in-where.md) put the inner query in WHERE (it handed over a list), this one hands over a whole table. the shop is the imaginary gujarati snack store these notes run on (orders table: 7 rows).

step one, the inner query alone, [GROUP BY](./143-group-by-one-group-per-value.md) making one row per customer, count(*) counting its rows:

```sql
SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | orders
1 | 3
2 | 2
3 | 1
4 | 1
```

step two, wrap it in parentheses, give it a [table alias](./158-table-aliases-short-nicknames-for-tables.md) (a short name for one query), and average the orders column:

```sql
SELECT avg(orders) AS avg_orders FROM (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) AS per_customer
```

```result
avg_orders
1.75
```

the outer query never sees the orders table, only those 4 rows. [avg](./140-sum-and-avg-adding-up-and-averaging.md) (sum divided by how many values) is 7 divided by 4. in python it is a list of per-customer counts first, then `sum(counts) / len(counts)`, two loops in a row.

the gotcha is Esha. she has no orders, so she has no group, so the 4 rows never include her. 1.75 is the average among customers who ordered; counting her would make it 7 over 5, which is 1.4. i expected the database to know about all 5 customers, but the inner query only knows what its FROM gave it.

any average of per-day or per-user totals works this way.

### check yourself

1. you add WHERE orders >= 2 to the outer query only. how many rows reach avg, and what does it return?
```sql
SELECT avg(orders) AS avg_orders FROM (SELECT customer_id, count(*) AS orders FROM orders GROUP BY customer_id) AS per_customer WHERE orders >= 2
```
<details><summary>answer</summary>

```result
avg_orders
2.5
```
2 rows reach avg, Asha with 3 and Bhavin with 2, so 5 divided by 2. the tempting answer is 1.75, from thinking the filter runs on the 7 order rows before grouping. it runs on the grouped table.

</details>

2. the owner only cares about delivered orders. you put WHERE status = 'delivered' inside the inner query. predict the average, rounded to 2 places.
```sql
SELECT round(avg(orders), 2) AS avg_delivered FROM (SELECT customer_id, count(*) AS orders FROM orders WHERE status = 'delivered' GROUP BY customer_id) AS per_customer
```
<details><summary>answer</summary>

```result
avg_delivered
1.67
```
only Asha (2), Bhavin (2) and Disha (1) have a delivered order, so 5 divided by 3. Chirag drops out of the inner table entirely. the tempting answer is 1.75, from keeping all 4 customers in the divisor.

</details>

---
prev: [174 subquery in WHERE](./174-subquery-in-where.md) | next: [176 scalar subqueries, one value inside a query](./176-scalar-subqueries-one-value-inside-a-query.md)
