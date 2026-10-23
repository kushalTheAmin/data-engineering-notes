# 171: joins plus GROUP BY, revenue per customer
builds on: [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [147 WHERE vs HAVING, before grouping or after](./147-where-vs-having-before-grouping-or-after.md), [154 capstone, orders per customer traced from rows to groups](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [163 joining three tables](./163-joining-three-tables.md)
section: combining tables with joins, part 17, ~2 min read

Chirag never got a delivered order, and the revenue report still says he spent 18.00. which part of the query is lying?

revenue per customer is a join chain followed by a GROUP BY. the joins build one row for every item bought, then the grouping collapses those rows into one line per customer. the shop (the imaginary gujarati snack store these notes run on) keeps names in customers, quantities in order_items and prices in products, so it takes a [chain of joins](./163-joining-three-tables.md) (each one pairs up rows that share an id) to get them onto one row. c, o, oi and p are table nicknames. [sum](./140-sum-and-avg-adding-up-and-averaging.md) (adds a column up) over quantity times price does the rest:

```sql
SELECT c.name, sum(oi.quantity * p.price) AS revenue FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY c.name
```

```result
name | revenue
Asha | 43.50
Bhavin | 28.00
Chirag | 18.00
Disha | 37.00
```

Ashas 43.50 is 5 joined rows added up: 12.00 and 6.00 (order 101), 7.50 and 3.00 (103), 15.00 (106). the joins run first, then [GROUP BY](./143-group-by-one-group-per-value.md) (one line per different value) runs on their output. Esha is missing because an [inner join](./156-inner-join-traced-by-hand.md) (keeps only matching pairs) drops anyone with no orders, like [154](./154-capstone-orders-per-customer-traced-from-rows-to-groups.md) found. and Chirags 18.00 is order 104, cancelled. nothing in a join knows about status, so you have to ask. a [WHERE](./147-where-vs-having-before-grouping-or-after.md) runs before the grouping, so it drops rows before they get summed:

```sql
SELECT c.name, sum(oi.quantity * p.price) AS revenue FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id WHERE o.status = 'delivered' GROUP BY c.name ORDER BY c.name
```

```result
name | revenue
Asha | 28.50
Bhavin | 28.00
Disha | 37.00
```

Asha lost her pending order 106 (15.00), and Chirag has no rows left. i kept thinking of revenue as a column that already exists, but nothing stores it, its one multiplication per joined row. check any revenue number for cancelled orders.

### check yourself

1. the owner wants revenue per product category instead, using the same chain without customers. the three category totals, added together, equal one number from above. which one, and why?
```sql
SELECT sum(revenue) AS total FROM (SELECT p.category, sum(oi.quantity * p.price) AS revenue FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY p.category)
```
<details><summary>answer</summary>

```result
total
126.50
```
the four customer revenues added up: 43.50 + 28.00 + 18.00 + 37.00. both groupings sum the same 13 joined rows, just bucketed differently. the tempting answer is something smaller like 28.50, from the delivered only query, but that one had a WHERE and this one doesnt.

</details>

2. to show Esha, who has no orders, a teammate makes only the first join a LEFT JOIN (keeps customers with no match, filling the order columns with NULL, a missing value) and leaves the other two as plain JOINs. how many lines come back?
```sql
SELECT c.name, sum(oi.quantity * p.price) AS revenue FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY c.name ORDER BY c.name
```
<details><summary>answer</summary>

```result
name | revenue
Asha | 43.50
Bhavin | 28.00
Chirag | 18.00
Disha | 37.00
```
4, no Esha. her filled in row has order_id NULL, and the next inner join tests it with =, which never matches a NULL ([166](./166-joining-on-columns-that-can-be-null.md)). the tempting answer is 5, since the left join already kept her. every join after a left join has to be a left join too.

</details>

---
prev: [170 joining on a range, matching a date to a period](./170-joining-on-a-range-matching-a-date-to-a-period.md) | next: [172 practice, five join questions on the shop, checking row counts](./172-practice-five-join-questions-on-the-shop-checking-row-counts.md)
