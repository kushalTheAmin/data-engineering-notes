# 207: capstone, each customers first order and the days between orders
builds on: [129 the difference between two dates](./129-the-difference-between-two-dates.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [141 what NULLs do to SUM and AVG](./141-what-nulls-do-to-sum-and-avg.md), [156 inner join traced by hand](./156-inner-join-traced-by-hand.md), [180 CTEs, naming each step with WITH](./180-ctes-naming-each-step-with-with.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [186 PARTITION BY, a separate window per group](./186-partition-by-a-separate-window-per-group.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md), [192 LAG and LEAD, looking at the row before](./192-lag-and-lead-looking-at-the-row-before.md)
section: bigger queries, wrap up, ~3 min read

Asha ordered on april 1, 3 and 8. which one was her first, and how long did she wait each time? [206](./206-practice-ten-interview-style-sql-questions-on-the-shop.md) was ten separate questions, and this one stacks several of this sections tools in one query.

the shop is the imaginary gujarati snack store these notes run on. the plan: a [CTE](./180-ctes-naming-each-step-with-with.md) (a named step) joins customers to their orders, then two [window functions](./184-window-functions-a-total-next-to-every-row.md) (calculations that keep every row) look through one window per customer, [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) name, sorted by day.

```text
customers JOIN orders             [156]       7 rows, one per order
the CTE o names that step         [180]
a window per customer, by day     [185, 186]
  row_number()        -> nth      [187]       1, 2, 3 inside each customer
  day - lag(day)      -> days_since [192, 129] gap to the row before
```

```sql
WITH o AS (SELECT c.name, CAST(o.ordered_at AS DATE) AS day, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id) SELECT name, order_id, day, row_number() OVER (PARTITION BY name ORDER BY day) AS nth, day - lag(day) OVER (PARTITION BY name ORDER BY day) AS days_since FROM o ORDER BY name, day
```

```result
name | order_id | day | nth | days_since
Asha | 101 | 2026-04-01 | 1 | NULL
Asha | 103 | 2026-04-03 | 2 | 2
Asha | 106 | 2026-04-08 | 3 | 5
Bhavin | 102 | 2026-04-01 | 1 | NULL
Bhavin | 107 | 2026-04-09 | 2 | 8
Chirag | 104 | 2026-04-04 | 1 | NULL
Disha | 105 | 2026-04-06 | 1 | NULL
```

the ORDER BY name, day at the end sorts the output rows. nth is [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md) (numbers rows 1, 2, 3 in window order), so a customers first order is the row where nth is 1. days_since is the day minus [LAG](./192-lag-and-lead-looking-at-the-row-before.md) (the value from the row before). [CAST](./132-cast-changing-a-values-type.md) (changes a values type) made the day a plain date, so the subtraction counts calendar days and ignores the clock, [129](./129-the-difference-between-two-dates.md). Asha waited 2 days, then 5.

every first order shows NULL (no value), because no row stands behind it, and 0 would be a lie, and you cant count a wait that never happened. Esha is missing completely, since an inner join (keeps only rows that match) drops customers with no orders. i figured the first order and the gap were two jobs, but the same sorted window hands out both.

the pieces, each with its note:
- subqueries: [in WHERE](./174-subquery-in-where.md), [in FROM](./175-subquery-in-from.md), [scalar](./176-scalar-subqueries-one-value-inside-a-query.md), [correlated](./177-correlated-subqueries-a-query-that-depends-on-the-outer-row.md)
- asking if a row exists: [EXISTS and NOT EXISTS](./178-exists-and-not-exists-asking-whether-a-matching-row-exists.md), [NOT IN and NULL](./179-not-in-and-the-null-trap.md)
- naming and stacking: [CTEs](./180-ctes-naming-each-step-with-with.md), [views](./181-views-a-saved-query-with-a-name.md), [UNION](./182-union-and-union-all.md), [INTERSECT and EXCEPT](./183-intersect-and-except.md)
- windows: [a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [OVER](./185-over-the-window-a-function-looks-through.md), [PARTITION BY](./186-partition-by-a-separate-window-per-group.md), [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md), [RANK and DENSE_RANK](./188-rank-vs-dense-rank-what-ties-do.md)
- running and frames: [running totals](./189-running-totals.md), [ROWS BETWEEN](./190-window-frames-rows-between.md), [the default frame trap](./191-the-default-frame-trap.md)
- neighbors and picks: [LAG and LEAD](./192-lag-and-lead-looking-at-the-row-before.md), [top N per group](./193-top-n-per-group.md), [removing duplicates](./194-removing-duplicates-with-row-number.md)
- streaks and time: [islands](./195-gaps-and-islands-date-minus-row-number.md), [one row per streak](./196-gaps-and-islands-one-row-per-streak.md), [generate_series](./197-generate-series-a-column-of-consecutive-days.md), [date spines](./198-date-spines-a-left-join-that-keeps-the-empty-days.md), [session starts](./199-session-starts-flag-the-click-after-a-long-gap.md), [session ids](./200-session-ids-a-running-sum-of-the-flags.md)
- who stays: [cohorts](./201-cohorts-the-month-each-customer-first-showed-up.md), [retention](./202-retention-who-came-back-the-month-after.md)
- other shapes: [recursive CTEs](./203-recursive-ctes-following-a-chain-of-rows.md), [arrays and UNNEST](./204-arrays-and-unnest-lists-inside-a-cell.md), [JSON in a column](./205-querying-json-inside-a-column.md)
- reps: [ten interview questions](./206-practice-ten-interview-style-sql-questions-on-the-shop.md)

the next section is about changing data, and what happens when two people do it at once.

### check yourself

1. order 104 is cancelled and 106 is pending. a teammate adds WHERE (keeps matching rows) o.status = 'delivered' inside the CTE. predict ashas last row. which customer disappears?
```sql
WITH o AS (SELECT c.name, CAST(o.ordered_at AS DATE) AS day, o.order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'delivered') SELECT name, order_id, day, row_number() OVER (PARTITION BY name ORDER BY day) AS nth, day - lag(day) OVER (PARTITION BY name ORDER BY day) AS days_since FROM o ORDER BY name, day
```
<details><summary>answer</summary>

```result
name | order_id | day | nth | days_since
Asha | 101 | 2026-04-01 | 1 | NULL
Asha | 103 | 2026-04-03 | 2 | 2
Bhavin | 102 | 2026-04-01 | 1 | NULL
Bhavin | 107 | 2026-04-09 | 2 | 8
Disha | 105 | 2026-04-06 | 1 | NULL
```
the WHERE runs before the windows, so pending order 106 never reaches them and Asha ends on order 103 with a gap of 2. Chirag disappears, his only order was cancelled. the tempting answer is 106 with a gap of 5, from forgetting the filter runs first.

</details>

2. what does avg(days_since) give for Asha, using the first query as a CTE?
```sql
WITH o AS (SELECT c.name, CAST(o.ordered_at AS DATE) AS day FROM customers c JOIN orders o ON c.customer_id = o.customer_id), g AS (SELECT name, day - lag(day) OVER (PARTITION BY name ORDER BY day) AS days_since FROM o) SELECT name, avg(days_since) AS avg_gap FROM g WHERE name = 'Asha' GROUP BY name
```
<details><summary>answer</summary>

```result
name | avg_gap
Asha | 3.5
```
avg skips the NULL ([141](./141-what-nulls-do-to-sum-and-avg.md)) and GROUP BY gives one bucket per name, so it is (2 + 5) / 2 = 3.5. the tempting answer is 2.33, from counting the first order as a 0 and dividing by 3.

</details>

---
prev: [206 practice, ten interview style SQL questions on the shop](./206-practice-ten-interview-style-sql-questions-on-the-shop.md) | next: [208 containers, a program packed with everything it needs](./208-containers-a-program-packed-with-everything-it-needs.md)
