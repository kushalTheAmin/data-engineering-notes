# 144: grouping by more than one column
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [137 aggregate functions, many rows in, one value out](./137-aggregate-functions-many-rows-in-one-value-out.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md)
section: summarizing data, part 8, ~2 min read

Asha, customer 1, has 3 orders. but are they 3 happy deliveries, or did one get stuck? can you tell from a count per customer? you cant.

in [143](./143-group-by-one-group-per-value.md) GROUP BY made one group per different value of one column. list two columns and a group is one different pair of values. in python the dictionary key becomes a pair, like (1, "delivered"). here are the 7 orders of the shop, the imaginary gujarati snack store these notes run on, counted per customer and status:

```sql
SELECT customer_id, status, count(*) AS n FROM orders GROUP BY customer_id, status ORDER BY customer_id, status
```

```result
customer_id | status | n
1 | delivered | 2
1 | pending | 1
2 | delivered | 2
3 | cancelled | 1
4 | delivered | 1
```

7 orders became 5 groups. Asha split into two rows, 2 delivered and 1 pending, so the stuck one is finally visible. each [aggregate](./137-aggregate-functions-many-rows-in-one-value-out.md) (many rows in, one value out) now runs per pair, and the counts add back up to 7.

i assumed i would get a row for every customer and status combo, 4 customers with orders times 3 statuses is 12. only the pairs that exist in the data show up, so customer 2 and cancelled has no row, not even a zero.

the order of the columns in GROUP BY doesnt change the groups, same 5 pairs either way. it only matters in [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) (sorting the rows), where it decides which column sorts first.

so what: revenue per day per product, signups per country per plan. adding a column makes the report finer, never smaller, so there are always at least as many rows as before.

### check yourself

1. from the 7 orders, the status-only count gives delivered 5, cancelled 1, pending 1. you add customer_id to the GROUP BY. can delivered end up with a count bigger than 5?
<details><summary>answer</summary>

no. splitting groups only cuts them into smaller pieces, so the 5 delivered orders spread over customers 1, 2 and 4 as 2, 2 and 1. the tempting answer is yes, from thinking more columns means more rows counted. it means more groups, each smaller.

</details>

2. predict how many rows come back, then count them.
```sql
SELECT customer_id, status, count(*) AS n FROM orders WHERE status <> 'pending' GROUP BY customer_id, status ORDER BY customer_id, status
```
<details><summary>answer</summary>

```result
customer_id | status | n
1 | delivered | 2
2 | delivered | 2
3 | cancelled | 1
4 | delivered | 1
```
4 rows, as WHERE runs first and removes the one pending order, so its pair never forms. the tempting answer is 5, from forgetting the filter happens before the grouping.

</details>

---
prev: [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md) | next: [145 the GROUP BY rule, every column is grouped or aggregated](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md)
