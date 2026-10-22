# 151: pivoting, turning rows into columns
builds on: [123 CASE WHEN, if and else inside a query](./123-case-when-if-and-else-inside-a-query.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [144 grouping by more than one column](./144-grouping-by-more-than-one-column.md), [148 conditional aggregation, counting several things in one pass](./148-conditional-aggregation-counting-several-things-in-one-pass.md)
section: summarizing data, part 15, ~2 min read

in [144](./144-grouping-by-more-than-one-column.md) Asha showed up on two lines, one for delivered and one for pending. a reader wants one line per customer, a column per status. how do you get there?

pivoting means taking the different values of one column and making each of them a column of its own. the data goes from long (many rows) to wide (many columns). here is the long shape, the orders of the shop, the imaginary gujarati snack store these notes run on, grouped by customer and status, n counting orders:

| customer_id | status | n |
|---|---|---|
| 1 | delivered | 2 |
| 1 | pending | 1 |
| 3 | cancelled | 1 |

(a slice, 3 of the 5 rows). and the wide shape, with one [conditional aggregation](./148-conditional-aggregation-counting-several-things-in-one-pass.md) (a CASE inside a sum) per status:

```sql
SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending, sum(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | delivered | pending | cancelled
1 | 2 | 1 | 0
2 | 2 | 0 | 0
3 | 0 | 0 | 1
4 | 1 | 0 | 0
```

in python it is one dictionary per customer with a counter per status. Asha is one row now: 2 delivered, 1 pending. and customer 2 with cancelled, a pair that had no row in [144](./144-grouping-by-more-than-one-column.md), is now a 0.

i assumed the columns would appear by themselves from whatever statuses the data holds. they dont, you type every one. leave a status out and its orders disappear from the columns, with no error:

```sql
SELECT customer_id, sum(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered, sum(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending, count(*) AS total FROM orders GROUP BY customer_id ORDER BY customer_id
```

```result
customer_id | delivered | pending | total
1 | 2 | 1 | 3
2 | 2 | 0 | 2
3 | 0 | 0 | 1
4 | 1 | 0 | 1
```

Chirag has total 1 but 0 and 0, his cancelled order has no column. a count(*) total beside them catches it.

so what: DuckDB, the database these notes run on, has a PIVOT statement that finds the values itself, `PIVOT orders ON status USING count(*) GROUP BY customer_id`, so a new status becomes a new column. the next one is about getting subtotal rows too.

---
prev: [150 percentiles, the medians cousins](./150-percentiles-the-medians-cousins.md) | next: [152 ROLLUP, subtotals and grand totals](./152-rollup-subtotals-and-grand-totals.md)
