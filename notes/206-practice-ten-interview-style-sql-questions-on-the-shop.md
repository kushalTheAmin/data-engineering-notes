# 206: practice, ten interview style SQL questions on the shop
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [115 IS NULL and IS NOT NULL](./115-is-null-and-is-not-null.md), [116 coalesce, a fallback when a value is null](./116-coalesce-a-fallback-when-a-value-is-null.md), [146 HAVING, filtering whole groups](./146-having-filtering-whole-groups.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [176 scalar subqueries, one value inside a query](./176-scalar-subqueries-one-value-inside-a-query.md), [178 EXISTS and NOT EXISTS, asking whether a matching row exists](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md), [180 CTEs, naming each step with WITH](./180-ctes-naming-each-step-with-with.md), [183 INTERSECT and EXCEPT](./183-intersect-and-except.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md), [189 running totals](./189-running-totals.md)
section: bigger queries, part 33, ~2 min read

the shop sells 6 products, so why does a units per product query list only 5? questions like that are what interviews love, and the SQL is rarely the hard part. the hard part is hearing which tool the question is asking for.

this is practice, ten questions on the shop (the imaginary gujarati snack store these notes run on), easy to hard, using the customers, orders, order_items and products tables (status, price, category and so on). this table is how i sort them now:

| the question says | reach for |
|---|---|
| only some rows | [WHERE](./106-where-keeping-only-the-rows-that-match.md), keeps rows passing a test |
| never, nobody | [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every row of the first table) plus [IS NULL](./115-is-null-and-is-not-null.md), or [NOT EXISTS](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md), no matching row exists |
| more than once | GROUP BY (one bucket per value) plus [HAVING](./146-having-filtering-whole-groups.md), filters buckets |
| second highest | [scalar subquery](./176-scalar-subqueries-one-value-inside-a-query.md), a query giving one value |
| both A and B | [INTERSECT](./183-intersect-and-except.md), rows two queries share |
| latest per customer | [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md), numbers rows in order |
| average of totals | [CTE](./180-ctes-naming-each-step-with-with.md), a named step, first |
| running | [running total](./189-running-totals.md), a sum that keeps growing |

worked example: how many orders are not delivered? <> means not equal, and 104 is cancelled, 106 is pending:

```sql
SELECT count(*) AS not_delivered FROM orders WHERE status <> 'delivered'
```

```result
not_delivered
2
```

i kept reading these as syntax puzzles, but half the work is deciding the shape of the answer before you type. tasks 3, 8 and 9 are the ones where the obvious query returns a believable wrong answer. for more reps, [DataLemur](https://datalemur.com) and [StrataScratch](https://www.stratascratch.com) have SQL interview questions.

### check yourself

1. how many orders are delivered?

<details><summary>answer</summary>

```sql
SELECT count(*) AS delivered FROM orders WHERE status = 'delivered'
```

```result
delivered
5
```



</details>

2. which customers have never ordered?

<details><summary>answer</summary>

```sql
SELECT c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL
```

```result
name
Esha
```

the filler row a left join adds has a NULL (no value) order_id, so IS NULL finds it.

</details>

3. units sold per product, and fafda must show up too.

<details><summary>answer</summary>

```sql
SELECT p.name, coalesce(sum(oi.quantity), 0) AS units FROM products p LEFT JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.name ORDER BY units DESC, p.name
```

```result
name | units
dhokla | 6
jalebi | 4
masala chai | 4
kaju katli | 3
khandvi | 3
fafda | 0
```

an inner join (keeps only matched rows) would drop fafda, nobody ordered it. [coalesce](./116-coalesce-a-fallback-when-a-value-is-null.md) turns its NULL sum into 0.

</details>

4. which product has the second highest price?

<details><summary>answer</summary>

```sql
SELECT name FROM products WHERE price = (SELECT max(price) FROM products WHERE price < (SELECT max(price) FROM products))
```

```result
name
khandvi
```

the inner query finds the top price, the middle one the best price below it.

</details>

5. which customers ordered more than once, and how many times?

<details><summary>answer</summary>

```sql
SELECT c.name, count(*) AS orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.name HAVING count(*) > 1 ORDER BY c.name
```

```result
name | orders
Asha | 3
Bhavin | 2
```

a WHERE cant do this, the count only exists after grouping.

</details>

6. who bought both a sweet and a snack?

<details><summary>answer</summary>

```sql
WITH bought AS (SELECT c.name, p.category FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id) SELECT name FROM bought WHERE category = 'sweet' INTERSECT SELECT name FROM bought WHERE category = 'snack'
```

```result
name
Bhavin
```

a WHERE category = 'sweet' AND category = 'snack' returns nothing, one row has one category.

</details>

7. each customers latest order.

<details><summary>answer</summary>

```sql
SELECT name, order_id FROM (SELECT c.name, o.order_id, row_number() OVER (PARTITION BY c.name ORDER BY o.ordered_at DESC) AS rn FROM customers c JOIN orders o ON c.customer_id = o.customer_id) WHERE rn = 1 ORDER BY name
```

```result
name | order_id
Asha | 106
Bhavin | 107
Chirag | 104
Disha | 105
```

newest first, number each customers orders (PARTITION BY restarts the count per customer), keep number 1.

</details>

8. customers who have orders and every one was delivered.

<details><summary>answer</summary>

```sql
SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status <> 'delivered') ORDER BY c.name
```

```result
name
Bhavin
Disha
```

the first EXISTS guards against Esha, who qualifies by having nothing undelivered.

</details>

9. average order value. try the obvious query first, then fix it.

<details><summary>answer</summary>

```sql
WITH t AS (SELECT o.order_id, sum(oi.quantity * p.price) AS total FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.order_id) SELECT round(avg(total), 2) AS avg_order FROM t
```

```result
avg_order
18.07
```

avg straight over the joined rows gives 9.73, the average item line. total each order first, then average the 7 totals (cancelled and pending orders count too).

</details>

10. the total per order, plus a running total in order id order.

<details><summary>answer</summary>

```sql
WITH t AS (SELECT o.order_id, sum(oi.quantity * p.price) AS total FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id GROUP BY o.order_id) SELECT order_id, total, sum(total) OVER (ORDER BY order_id) AS running FROM t ORDER BY order_id
```

```result
order_id | total | running
101 | 18.00 | 18.00
102 | 17.00 | 35.00
103 | 10.50 | 45.50
104 | 18.00 | 63.50
105 | 37.00 | 100.50
106 | 15.00 | 115.50
107 | 11.00 | 126.50
```

the CTE makes one total per order, then the running sum adds those up in order. order 104 is cancelled but still in the sum.

</details>

---
prev: [205 querying JSON inside a column](./205-querying-json-inside-a-column.md) | next: [207 capstone, each customers first order and the days between orders](./207-capstone-each-customers-first-order-and-the-days-between-orders.md)
