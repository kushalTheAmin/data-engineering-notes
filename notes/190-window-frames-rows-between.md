# 190: window frames, ROWS BETWEEN
builds on: [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [175 subquery in FROM](./175-subquery-in-from.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md), [189 running totals](./189-running-totals.md)
section: bigger queries, part 17, ~2 min read

one day of orders is jumpy, april 2 has 0 and april 1 has 2. i wanted the last 3 days added up on every row, and a running total cant do that.

a window frame is the slice of the [window](./185-over-the-window-a-function-looks-through.md) (the rows a function sees) that it actually adds up for the current row. ROWS BETWEEN 2 PRECEDING AND CURRENT ROW means this row plus the 2 rows before it, in the order of the ORDER BY (sorts rows). the shop, the imaginary snack store these notes run on, has daily_orders from [130](./130-nullif-and-dividing-by-zero.md), one row per day:

```sql
SELECT day, placed, sum(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3, sum(placed) OVER (ORDER BY day) AS running FROM daily_orders ORDER BY day
```

```result
day | placed | last3 | running
2026-04-01 | 2 | 2 | 2
2026-04-02 | 0 | 2 | 2
2026-04-03 | 1 | 3 | 3
2026-04-04 | 1 | 2 | 4
2026-04-05 | 0 | 2 | 4
2026-04-06 | 1 | 2 | 5
2026-04-07 | 0 | 1 | 5
2026-04-08 | 1 | 2 | 6
2026-04-09 | 1 | 2 | 7
```

in python, last3 on row i is sum(placed[max(0, i-2):i+1]). april 6 is 2 because its frame is april 4, 5 and 6, and 1 + 0 + 1 = 2. the first rows have fewer rows to use, so april 1 is just itself. the running column from [189](./189-running-totals.md) is a frame too, one that starts at the first row.

i expected the frame to count days, but it counts rows. here every day has a row so it works out, but if you lose a day, 2 PRECEDING reaches one day further back. WHERE (keeps matching rows) removing a row does the same.

avg over this frame on april 1 gives 2.0, not 0.67, because it divides by the 1 row it has. Postgres documents the same ROWS BETWEEN.

### check yourself

1. predict both rows. the inner query is a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT used as a table).
```sql
SELECT day, s FROM (SELECT day, sum(placed) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS s FROM daily_orders) AS t WHERE day IN (DATE '2026-04-02', DATE '2026-04-06') ORDER BY day
```
<details><summary>answer</summary>

```result
day | s
2026-04-02 | 3
2026-04-06 | 1
```
the frame is the row before, the row itself and the row after. april 6 is 0 + 1 + 0 = 1. the tempting answer is 0, from leaving out the current row.

</details>

2. this drops april 5 before the window runs. what does april 6 show for the 3 row frame?
```sql
SELECT day, sum(placed) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS last3 FROM daily_orders WHERE day = DATE '2026-04-06' OR day < DATE '2026-04-05'
```
<details><summary>answer</summary>

```result
day | last3
2026-04-01 | 2
2026-04-02 | 2
2026-04-03 | 3
2026-04-04 | 2
2026-04-06 | 3
```
april 5 is gone, so the 2 rows before april 6 are april 3 and 4, and 1 + 1 + 1 = 3. the tempting answer is 2, from thinking of april 4, 5 and 6 as three days.

</details>

---
prev: [189 running totals](./189-running-totals.md) | next: [191 the default frame trap](./191-the-default-frame-trap.md)
