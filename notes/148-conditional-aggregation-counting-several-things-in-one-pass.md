# 148: conditional aggregation, counting several things in one pass
builds on: [123 CASE WHEN, if and else inside a query](./123-case-when-if-and-else-inside-a-query.md), [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [147 WHERE vs HAVING, before grouping or after](./147-where-vs-having-before-grouping-or-after.md)
section: summarizing data, part 12, ~2 min read

in [147](./147-where-vs-having-before-grouping-or-after.md) WHERE threw rows away before counting, so Asha, who has 3 orders, counted only 2. so how do you get delivered, pending and total side by side, when WHERE can only keep one slice?

you put the decision inside the aggregate. [CASE WHEN](./123-case-when-if-and-else-inside-a-query.md) (an if per row) hands back 1 when the row matches and 0 when it doesnt, and [sum](./140-sum-and-avg-adding-up-and-averaging.md) (adds up a column) adds those. in python it is a loop with several counters, `if status == "delivered": delivered += 1`, and every row still goes through every counter. here are the orders of the shop, the imaginary gujarati snack store these notes run on, one row per [customer](./143-group-by-one-group-per-value.md):

```sql
SELECT customer_id, count(*) AS total, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | total | delivered | pending
1 | 3 | 2 | 1
2 | 2 | 2 | 0
3 | 1 | 0 | 0
4 | 1 | 1 | 0
```

nothing was filtered, so Asha, customer 1, keeps all 3 orders in total and also shows her 2 delivered and 1 pending. customer 3 is back too, with zeros, where in 147 they had no group at all. i assumed a filter always meant losing rows, and this one filters inside the number, not on the rows.

now the trap. [count(column)](./138-count-star-vs-count-of-a-column.md) (counts rows where the value is not null, a null being a missing value) with the same CASE:

```sql
SELECT count(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS wrong, count(CASE WHEN status = 'pending' THEN 1 END) AS right FROM orders
```

```result
wrong | right
7 | 1
```

0 is a value, so the ELSE 0 version counts every row. drop the ELSE and non-matching rows become null, which count skips.

so what: one pass over the table gives a whole report row, instead of one query per number. the next one is about the middle value, the median.

### check yourself

1. without running it, what does this return, and why isnt it the number of delivered orders?
```sql
SELECT count(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS c FROM orders
```
<details><summary>answer</summary>

```result
c
7
```
ELSE 0 gives every non-delivered row a 0, and count counts any value that isnt null, so all 7 orders count. delivered is 5 and needs sum, or no ELSE. the tempting answer is 5, from reading the CASE as a filter.

</details>

2. what comes back for customers 2 and 3? there is no ELSE here, so non-matching rows become null, and sum skips nulls.
```sql
SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 END) AS delivered FROM orders WHERE customer_id IN (2, 3) GROUP BY customer_id ORDER BY customer_id
```
<details><summary>answer</summary>

```result
customer_id | delivered
2 | 2
3 | NULL
```
customer 3 has one cancelled order, so every CASE inside their group is null, and sum over only nulls is NULL, not 0. wrap it in COALESCE ([116](./116-coalesce-a-fallback-when-a-value-is-null.md), a fallback for null) to get 0. the tempting answer is 0.

</details>

---
prev: [147 WHERE vs HAVING, before grouping or after](./147-where-vs-having-before-grouping-or-after.md) | next: not written yet
