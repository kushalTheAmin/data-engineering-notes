# 191: the default frame trap, why ORDER BY turns MAX into a running max
builds on: [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [142 min and max, the smallest and biggest value](./142-min-and-max-the-smallest-and-biggest-value.md), [175 subquery in FROM](./175-subquery-in-from.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [189 running totals](./189-running-totals.md), [190 window frames, ROWS BETWEEN](./190-window-frames-rows-between.md)
section: bigger queries, part 18, ~2 min read

i added an ORDER BY (sorts rows) inside [OVER](./185-over-the-window-a-function-looks-through.md) (which rows a function sees) to a max and the answer changed, and i hadnt asked for a running anything. has this happened to you?

the default frame trap: if OVER has an ORDER BY and no frame, the [frame](./190-window-frames-rows-between.md) (the slice of rows a function uses) quietly becomes "the first row up to this one". so [max](./142-min-and-max-the-smallest-and-biggest-value.md) (the biggest value) turns into a running max. here is the cancelled count from daily_orders, the shops one row per day (the shop is the imaginary snack store these notes run on, table from [130](./130-nullif-and-dividing-by-zero.md)):

```sql
SELECT day, cancelled, max(cancelled) OVER () AS all_max, max(cancelled) OVER (ORDER BY day) AS with_order, max(cancelled) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS whole FROM daily_orders ORDER BY day
```

```result
day | cancelled | all_max | with_order | whole
2026-04-01 | 0 | 1 | 0 | 1
2026-04-02 | 0 | 1 | 0 | 1
2026-04-03 | 0 | 1 | 0 | 1
2026-04-04 | 1 | 1 | 1 | 1
2026-04-05 | 0 | 1 | 1 | 1
2026-04-06 | 0 | 1 | 1 | 1
2026-04-07 | 0 | 1 | 1 | 1
2026-04-08 | 0 | 1 | 1 | 1
2026-04-09 | 0 | 1 | 1 | 1
```

with_order stays 0 until april 4, the day of the only cancellation, because before that the frame hasnt seen it. it is the [running total](./189-running-totals.md) idea, with max. a bare OVER () has no ORDER BY, so its frame is every row left after WHERE (keeps matching rows). rows tied in the ORDER BY share a frame, but the shops days never tie. to keep the ORDER BY and still see everything, say so: UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING (no limit either way).

i assumed the sorting only decided the order, but it also shrinks what the function can see.

it bites hardest with last_value, which returns the value at the last row of the frame. with just ORDER BY day it hands back the current rows own value, so with the placed column, april 5 shows 0 instead of the last days 1. Postgres docs say the same.

### check yourself

1. predict both rows. the inner query is a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT used as a table).
```sql
SELECT day, s FROM (SELECT day, min(placed) OVER (ORDER BY day) AS s FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-09') ORDER BY day
```
<details><summary>answer</summary>

```result
day | s
2026-04-01 | 2
2026-04-09 | 0
```
april 1 has only itself in its frame, so its min is 2. by april 9 the frame has seen the 0 on april 2. the tempting answer is 0 on both rows, from reading min as the min of the whole table.

</details>

2. this should show the last days placed count on every row. what do april 1 and april 5 show?
```sql
SELECT day, v FROM (SELECT day, last_value(placed) OVER (ORDER BY day) AS v FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-05') ORDER BY day
```
<details><summary>answer</summary>

```result
day | v
2026-04-01 | 2
2026-04-05 | 0
```
the frame ends at the current row, so last_value is the row itself. the tempting answer is 1 and 1, the placed count of april 9, which needs the UNBOUNDED FOLLOWING frame.

</details>

---
prev: [190 window frames, ROWS BETWEEN](./190-window-frames-rows-between.md) | next: [192 LAG and LEAD, looking at the row before](./192-lag-and-lead-looking-at-the-row-before.md)
