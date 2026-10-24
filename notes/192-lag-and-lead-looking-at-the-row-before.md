# 192: LAG and LEAD, looking at the row before
builds on: [031 NULL](./031-null.md), [117 ORDER BY, sorting by one or more columns](./117-order-by-sorting-by-one-or-more-columns.md), [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [189 running totals](./189-running-totals.md), [190 window frames, ROWS BETWEEN](./190-window-frames-rows-between.md)
section: bigger queries, part 19, ~2 min read

did the shop get busier today than yesterday? a running total cant say, it only adds, and i didnt want a self join (matching a table against a copy of itself) just to see one row back.

LAG and LEAD are window functions (SQL calculations across rows that still return every row) that hand you a value from another row: LAG from the row before, LEAD from the row after. the order comes from the ORDER BY (sorts rows) inside [OVER](./185-over-the-window-a-function-looks-through.md) (the part saying which rows a function sees). the shop, the imaginary snack store these notes run on, has daily_orders from [130](./130-nullif-and-dividing-by-zero.md), one row per day:

```sql
SELECT day, placed, lag(placed) OVER (ORDER BY day) AS before, lead(placed) OVER (ORDER BY day) AS after, placed - lag(placed) OVER (ORDER BY day) AS change FROM daily_orders ORDER BY day
```

```result
day | placed | before | after | change
2026-04-01 | 2 | NULL | 0 | NULL
2026-04-02 | 0 | 2 | 1 | -2
2026-04-03 | 1 | 0 | 1 | 1
2026-04-04 | 1 | 1 | 0 | 0
2026-04-05 | 0 | 1 | 1 | -1
2026-04-06 | 1 | 0 | 0 | 1
2026-04-07 | 0 | 1 | 1 | -1
2026-04-08 | 1 | 0 | 1 | 1
2026-04-09 | 1 | 1 | NULL | 0
```

read the before column and it is just the placed column pushed down one row. after is pushed up one. the first day has no row before it, so its before is [NULL](./031-null.md) (no value), and so is its change. the last day has nothing after it. i half expected an error or a 0 there, and it quietly gives NULL. you can ask for another distance, lag(placed, 2), or a stand-in for the missing first row, lag(placed, 1, 0).

the catch, same as in [190](./190-window-frames-rows-between.md): before means the row before in the ORDER BY, not the day before. if a day is missing, LAG just reaches over the gap.

this is how day over day change gets computed in SQL, one line instead of a self join.

### check yourself

1. WHERE (keeps matching rows) trims the shop to two days, then LAG runs. what do april 4 and april 6 show as before?
```sql
SELECT day, lag(placed) OVER (ORDER BY day) AS before FROM daily_orders WHERE day IN (DATE '2026-04-04', DATE '2026-04-06') ORDER BY day
```
<details><summary>answer</summary>

```result
day | before
2026-04-04 | NULL
2026-04-06 | 1
```
the WHERE runs first, so only 2 rows reach the window and april 6 looks back at april 4, whose placed is 1. the tempting answer is 0, april 5s value, from thinking LAG sees the whole table.

</details>

2. what does lag(placed, 2) show on april 2 and april 3?
```sql
SELECT day, two_back FROM (SELECT day, lag(placed, 2) OVER (ORDER BY day) AS two_back FROM daily_orders) AS t WHERE day IN (DATE '2026-04-02', DATE '2026-04-03') ORDER BY day
```
<details><summary>answer</summary>

```result
day | two_back
2026-04-02 | NULL
2026-04-03 | 2
```
with a distance of 2, the first two rows have nobody that far back, so both edges are NULL, but april 3 does reach april 1. the tempting answer is 0 on april 3, april 2s value, from reading 2 as one row back.

</details>

---
prev: [191 the default frame trap, why ORDER BY turns MAX into a running max](./191-the-default-frame-trap.md) | next: not written yet
