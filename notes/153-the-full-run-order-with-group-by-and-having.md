# 153: the full run order with GROUP BY and HAVING
builds on: [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [120 LIMIT and OFFSET, paging through rows](./120-limit-and-offset-paging-through-rows.md), [134 the order SQL really runs in](./134-the-order-sql-really-runs-in.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [146 HAVING, filtering whole groups](./146-having-filtering-whole-groups.md), [147 WHERE vs HAVING, before grouping or after](./147-where-vs-having-before-grouping-or-after.md)
section: summarizing data, part 17, ~2 min read

a query with WHERE, GROUP BY, HAVING, ORDER BY and LIMIT all at once: which one runs first, and does LIMIT cut rows or groups?

in [134](./134-the-order-sql-really-runs-in.md) i said the order is FROM, WHERE, SELECT, ORDER BY, LIMIT. the fuller picture is that [GROUP BY](./143-group-by-one-group-per-value.md) (one row per different value) and [HAVING](./146-having-filtering-whole-groups.md) (filters whole groups) slot in right after WHERE, before SELECT.

here is one query on the orders of the shop, the imaginary gujarati snack store these notes run on, traced step by step:

| step | clause | what is left |
|---|---|---|
| 1 | FROM orders | 7 rows |
| 2 | WHERE status <> 'cancelled' | 6 rows, order 104 is gone |
| 3 | GROUP BY customer_id | 3 groups: customer 1 has 3 rows, 2 has 2, 4 has 1 |
| 4 | HAVING count(*) >= 2 | 2 groups, customer 4 is gone |
| 5 | SELECT customer_id, count(*) AS n | 2 rows, n exists now: 3 and 2 |
| 6 | ORDER BY n DESC | customer 1, then 2 |
| 7 | LIMIT 1 | 1 row, customer 1 |

```sql
SELECT customer_id, count(*) AS n FROM orders WHERE status <> 'cancelled' GROUP BY customer_id HAVING count(*) >= 2 ORDER BY n DESC LIMIT 1
```

```result
customer_id | n
1 | 3
```

the order is [WHERE](./106-where-keeping-only-the-rows-that-match.md) on rows, groups, HAVING on groups, then SELECT, [ORDER BY](./117-order-by-sorting-by-one-or-more-columns.md) and [LIMIT](./120-limit-and-offset-paging-through-rows.md) on whatever groups survived. so LIMIT counts groups here, not orders.

i kept reading the query top to bottom, and it works like a pipe going WHERE to HAVING to the rest, each step handing less to the next.

the gotcha: SELECT runs after HAVING, so n doesnt exist yet at step 4. the docs of Postgres, a server database, say an output name works in ORDER BY but not in HAVING, so you repeat count(*). DuckDB, the database these notes run in, lets HAVING n work, but dont count on that elsewhere.

### check yourself

1. predict the single row. then say which wrong row you would get if HAVING ran after LIMIT.
```sql
SELECT customer_id, count(*) AS n FROM orders GROUP BY customer_id HAVING count(*) >= 2 ORDER BY n, customer_id LIMIT 1
```
<details><summary>answer</summary>

```result
customer_id | n
2 | 2
```
HAVING drops customers 3 and 4 (one order each) before the sort, so the smallest survivor is customer 2. if LIMIT ran earlier, the sort would put customer 3 with n = 1 first. the tempting answer is 3 | 1, from sorting all 4 groups.

</details>

2. in step 2, what would change if the WHERE were moved into HAVING as `HAVING status <> 'cancelled'`?
<details><summary>answer</summary>

it would error. after grouping, a group can hold several statuses and status is neither grouped nor aggregated, the rule from [145](./145-the-group-by-rule-every-column-is-grouped-or-aggregated.md). the tempting answer is that it gives the same rows, from treating the two filters as the same thing.

</details>

---
prev: [152 ROLLUP, subtotals and grand totals](./152-rollup-subtotals-and-grand-totals.md) | next: not written yet
