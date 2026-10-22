# 154: capstone, orders per customer traced from rows to groups
builds on: [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [138 COUNT star vs COUNT of a column](./138-count-star-vs-count-of-a-column.md), [139 COUNT DISTINCT, counting different values](./139-count-distinct-counting-different-values.md), [140 SUM and AVG, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md), [142 MIN and MAX, the smallest and biggest value](./142-min-and-max-the-smallest-and-biggest-value.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [144 grouping by more than one column](./144-grouping-by-more-than-one-column.md), [145 the GROUP BY rule, every column is grouped or aggregated](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md), [146 HAVING, filtering whole groups](./146-having-filtering-whole-groups.md), [147 WHERE vs HAVING, before grouping or after](./147-where-vs-having-before-grouping-or-after.md), [148 conditional aggregation, counting several things in one pass](./148-conditional-aggregation-counting-several-things-in-one-pass.md), [149 median, the middle value after sorting](./149-median-the-middle-value-after-sorting.md), [150 percentiles, the medians cousins](./150-percentiles-the-medians-cousins.md), [151 pivoting, turning rows into columns](./151-pivoting-turning-rows-into-columns.md), [152 ROLLUP, subtotals and grand totals](./152-rollup-subtotals-and-grand-totals.md), [153 the full run order with GROUP BY and HAVING](./153-the-full-run-order-with-group-by-and-having.md)
section: summarizing data, wrap up, ~3 min read

the shop has 5 customers, so why does a report of orders per customer come back with 4 rows? the last section ended on [136](./136-capstone-one-query-traced-clause-by-clause.md), queries that return rows, and this one is about queries that squash them.

an aggregate (many rows in, one value out, [137](./137-aggregate-functions-many-rows-in-one-value-out.md)) plus GROUP BY (one group per different value, [143](./143-group-by-one-group-per-value.md)) turns thousands of rows into the few numbers someone asked for. here is the whole thing on the orders of the shop, the imaginary gujarati snack store these notes run on. the left side is the 7 rows going in, the right side is what each group becomes:

```text
GROUP BY customer_id             then per group:
customer 1  orders 101 103 106   count 3, delivered 2, latest apr 8
customer 2  orders 102 107       count 2, delivered 2, latest apr 9
customer 3  orders 104           count 1, delivered 0, latest apr 4
customer 4  orders 105           count 1, delivered 1, latest apr 6
customer 5  no orders            no group at all
```

```sql
SELECT customer_id, count(*) AS orders, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, max(ordered_at) AS latest FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | orders | delivered | latest
1 | 3 | 2 | 2026-04-08 10:00:00
2 | 2 | 2 | 2026-04-09 13:45:00
3 | 1 | 0 | 2026-04-04 08:30:00
4 | 1 | 1 | 2026-04-06 19:10:00
```

the sum(CASE ...) is [148](./148-conditional-aggregation-counting-several-things-in-one-pass.md), an if per row that adds 1 for each delivered order. nothing is filtered out, so Chirag shows a 0 here, where a WHERE in [147](./147-where-vs-having-before-grouping-or-after.md) left him with no line. customer 1 is Asha, 2 is Bhavin, 3 is Chirag, 4 is Disha. Esha, customer 5, has no order rows, and a group is made from rows, so she gets no line. i expected a missing customer to show up as a zero, but you cant count rows that dont exist.

the pieces, each with its note:
- counting: [count(*) vs count(column)](./138-count-star-vs-count-of-a-column.md), [count distinct](./139-count-distinct-counting-different-values.md)
- adding: [sum and avg](./140-sum-and-avg-adding-up-and-averaging.md), [what nulls do to them](./141-what-nulls-do-to-sum-and-avg.md), [min and max](./142-min-and-max-the-smallest-and-biggest-value.md)
- grouping: [two columns](./144-grouping-by-more-than-one-column.md), [the rule](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md)
- filtering: [HAVING](./146-having-filtering-whole-groups.md), [WHERE vs HAVING](./147-where-vs-having-before-grouping-or-after.md)
- reshaping: [conditional aggregation](./148-conditional-aggregation-counting-several-things-in-one-pass.md), [pivoting](./151-pivoting-turning-rows-into-columns.md), [ROLLUP](./152-rollup-subtotals-and-grand-totals.md)
- middles: [median](./149-median-the-middle-value-after-sorting.md), [percentiles](./150-percentiles-the-medians-cousins.md)
- order: [WHERE, GROUP BY, HAVING, then SELECT](./153-the-full-run-order-with-group-by-and-having.md)

when a number looks wrong, ask what the rows were before they became groups. the next section brings Esha back, by combining tables.

### check yourself

1. the owner wants average items per order from order_items, the shop table with 13 rows, one per product per order, each with a quantity. which column is items per order, and why is the other wrong?
```sql
SELECT round(sum(quantity) / count(DISTINCT order_id), 2) AS a, round(avg(quantity), 2) AS b FROM order_items
```
<details><summary>answer</summary>

```result
a | b
2.86 | 1.54
```
a is right: 20 items over 7 orders. b is the average per row, and a row is one product in an order, 13 of them. the tempting answer is b, because avg sounds like the average of everything.

</details>

2. a teammate wants the report to show all 5 customers, with 0 for Esha, and says to add HAVING count(*) >= 0. does that work, and what does count(DISTINCT customer_id) say?
```sql
SELECT count(DISTINCT customer_id) AS with_orders FROM orders
```
<details><summary>answer</summary>

```result
with_orders
4
```
no. HAVING only filters groups that exist, and Esha has no rows to make one, so 4 is all the grouping can see. she needs the customers table brought in. the tempting answer is that count(*) >= 0 pulls her in, because 0 sounds like it covers her.

</details>

---
prev: [153 the full run order with GROUP BY and HAVING](./153-the-full-run-order-with-group-by-and-having.md) | next: not written yet
