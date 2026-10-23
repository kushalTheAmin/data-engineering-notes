# 172: practice, five join questions on the shop, checking row counts
builds on: [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [139 count distinct, counting different values](./139-count-distinct-counting-different-values.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [161 a WHERE that quietly turns a left join into an inner join](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md), [163 joining three tables](./163-joining-three-tables.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [171 joins plus GROUP BY, revenue per customer](./171-joins-plus-group-by-revenue-per-customer.md)
section: combining tables with joins, part 18, ~2 min read

your join (pairs up rows from two tables) ran and the total looks plausible. but did the join quietly copy or drop rows before anything got added up?

this one is practice, and the skill is a habit: say the row count out loud before you run a join, then check it. the shop (the imaginary gujarati snack store these notes run on) makes it easy, and it pays off in the [revenue chains](./171-joins-plus-group-by-revenue-per-customer.md) and [three table joins](./163-joining-three-tables.md) from before. when each order has exactly one customer, an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) returns one row per order, since every order in the shop has a customer. a [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every row of the table written first) adds one row for each left row with no partner (here every left row has at most one).

here is the slice you need, 5 customers (Asha, Bhavin, Chirag, Disha, Esha) and the 7 orders with how many items each holds:

| order_id | customer | items in it |
|---|---|---|
| 101 | Asha | 2 |
| 102 | Bhavin | 2 |
| 103 | Asha | 2 |
| 104 | Chirag | 1 |
| 105 | Disha | 3 |
| 106 | Asha | 1 |
| 107 | Bhavin | 2 |

| join | rows out | why |
|---|---|---|
| customers JOIN orders | 7 | one row per order, Esha has none |
| orders JOIN order_items | 13 | one row per item, orders [fan out](./164-fan-out-when-a-join-multiplies-rows.md) (get copied) |
| customers LEFT JOIN orders | 8 | the 7 orders plus a filler row for Esha |

Asha has 3 orders, so she becomes 3 rows. i figured counting rows was a beginner check, but its the first check that catches a join copying or dropping rows, before any sum does. it wont catch a wrong ON that keeps the same count. all tasks use customers, orders, order_items and products. for more reps, [DataLemur](https://datalemur.com) and [StrataScratch](https://www.stratascratch.com) have SQL interview questions.

### check yourself

1. predict the row count of customers LEFT JOIN orders LEFT JOIN order_items, then write the query.

<details><summary>answer</summary>

```sql
SELECT count(*) AS n FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id LEFT JOIN order_items oi ON o.order_id = oi.order_id
```

```result
n
14
```

13 item rows plus one filler row for Esha (every order has at least one item, or it would add a filler row too). the tempting answers are 13, forgetting Esha, or 8, stopping at the first join.

</details>

2. one query, on customers LEFT JOIN orders: the row count and the number of real orders. which is bigger?

<details><summary>answer</summary>

```sql
SELECT count(*) AS joined_rows, count(o.order_id) AS orders FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
```

```result
joined_rows | orders
8 | 7
```

count(*) counts Eshas filler row, [count of a column](./138-count-star-vs-count-of-a-column.md) skips her NULL (missing) order_id. the tempting answer is 7 for both.

</details>

3. over customers JOIN orders JOIN order_items, show each customers joined rows next to their different orders.

<details><summary>answer</summary>

```sql
SELECT c.name, count(*) AS joined_rows, count(DISTINCT o.order_id) AS orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.name ORDER BY c.name
```

```result
name | joined_rows | orders
Asha | 5 | 3
Bhavin | 4 | 2
Chirag | 1 | 1
Disha | 3 | 1
```

the tempting answer is that orders equal joined rows. Disha has one order with 3 items, so 3 rows. count(*) here counts items, and [count distinct](./139-count-distinct-counting-different-values.md) (counts different values) counts orders.

</details>

4. delivered revenue for all 5 customers, 0.00 for those with nothing delivered. a WHERE on status would lose rows, so where does the test go?

<details><summary>answer</summary>

```sql
SELECT c.name, coalesce(sum(oi.quantity * p.price), 0) AS revenue FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'delivered' LEFT JOIN order_items oi ON o.order_id = oi.order_id LEFT JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY c.name
```

```result
name | revenue
Asha | 28.50
Bhavin | 28.00
Chirag | 0.00
Disha | 37.00
Esha | 0.00
```

the test goes in the ON of the join to orders, and the later joins stay LEFT too, so Chirag and Esha survive. that way [161](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md) doesnt bite. a WHERE leaves only 3 customers, the tempting answer.

</details>

5. customers who bought a sweet. predict the joined row count before any DISTINCT, and how many different customers that is.

<details><summary>answer</summary>

```sql
SELECT count(*) AS joined_rows, count(DISTINCT c.name) AS customers FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE p.category = 'sweet'
```

```result
joined_rows | customers
5 | 2
```

5 sweet rows from order_items, bought by Bhavin and Disha. the tempting answer is 2 rows, but the join makes one per order_items row.

</details>

---
prev: [171 joins plus GROUP BY, revenue per customer](./171-joins-plus-group-by-revenue-per-customer.md) | next: not written yet
