# 152: ROLLUP, subtotals and grand totals
builds on: [031 null, a marker for a missing value](./031-null.md), [119 where nulls land when you sort](./119-where-nulls-land-when-you-sort.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [144 grouping by more than one column](./144-grouping-by-more-than-one-column.md), [151 pivoting, turning rows into columns](./151-pivoting-turning-rows-into-columns.md)
section: summarizing data, part 16, ~2 min read

counting orders per customer and status, as in [144](./144-grouping-by-more-than-one-column.md), shows Asha, customer 1, as 2 delivered and 1 pending, but where is her 3, or the shops total of 7? can the same query add those rows for you?

ROLLUP is a [GROUP BY](./143-group-by-one-group-per-value.md) (one group per value) that also adds a subtotal row per customer and one grand total row. here are the 7 orders of the shop, the imaginary gujarati snack store these notes run on, grouped with `ROLLUP (customer_id, status)`. NULLS LAST sorts the [NULL](./031-null.md) rows (a marker for a missing value) to the end of each customer, as in [119](./119-where-nulls-land-when-you-sort.md):

```sql
SELECT customer_id, status, count(*) AS n FROM orders GROUP BY ROLLUP (customer_id, status) ORDER BY customer_id NULLS LAST, status NULLS LAST
```

```result
customer_id | status | n
1 | delivered | 2
1 | pending | 1
1 | NULL | 3
2 | delivered | 2
2 | NULL | 2
3 | cancelled | 1
3 | NULL | 1
4 | delivered | 1
4 | NULL | 1
NULL | NULL | 7
```

10 rows: the 5 pairs from 144, 4 subtotals, 1 grand total. in python it is the same grouping loop run 3 times: by both columns, by customer alone, then by nothing, which is one group of everything. Asha is 2 + 1 = 3, and the 7 at the bottom is the whole shop.

i expected the totals to need a second query glued under the first. its the same query with one word wrapped around the columns.

the catch is that NULL here means "all of them", and a real missing status would look identical. the grouping() function tells them apart, 1 on a row the database added, 0 on a real group:

```sql
SELECT customer_id, count(*) AS n, grouping(customer_id) AS is_total FROM orders GROUP BY ROLLUP (customer_id) ORDER BY customer_id NULLS LAST
```

```result
customer_id | n | is_total
1 | 3 | 0
2 | 2 | 0
3 | 1 | 0
4 | 1 | 0
NULL | 7 | 1
```

so what: this is the totals row of most sales reports, and Postgres, a server database, has ROLLUP too. swap the two columns and the subtotals are per status instead, delivered 5.

---
prev: [151 pivoting, turning rows into columns](./151-pivoting-turning-rows-into-columns.md) | next: [153 the full run order with GROUP BY and HAVING](./153-the-full-run-order-with-group-by-and-having.md)
