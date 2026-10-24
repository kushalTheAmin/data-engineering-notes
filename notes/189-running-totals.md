# 189: running totals
builds on: [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [140 sum and avg, adding up and averaging](./140-sum-and-avg-adding-up-and-averaging.md), [175 subquery in FROM](./175-subquery-in-from.md), [184 window functions, a total next to every row](./184-window-functions-a-total-next-to-every-row.md), [185 OVER, the window a function looks through](./185-over-the-window-a-function-looks-through.md)
section: bigger queries, part 16, ~2 min read

how many orders has the shop taken so far, as of each day? in python i would keep a total and add to it in a loop, and i wanted that in one SQL line.

a running total is a [sum](./140-sum-and-avg-adding-up-and-averaging.md) where each row adds up itself and every row before it. you get it by putting an ORDER BY inside the [OVER](./185-over-the-window-a-function-looks-through.md) of a [window function](./184-window-functions-a-total-next-to-every-row.md) (a calculation that keeps every row). the shop, the imaginary snack store these notes run on, has daily_orders from [130](./130-nullif-and-dividing-by-zero.md), one row per day, with a placed and a cancelled count. in python:

```python
placed = [2, 0, 1, 1, 0, 1, 0, 1, 1]
total = 0
for p in placed:
    total += p
    print(total, end=" ")
```

```output
2 2 3 4 4 5 5 6 7 
```

and in SQL:

```sql
SELECT day, placed, sum(placed) OVER (ORDER BY day) AS running FROM daily_orders ORDER BY day
```

```result
day | placed | running
2026-04-01 | 2 | 2
2026-04-02 | 0 | 2
2026-04-03 | 1 | 3
2026-04-04 | 1 | 4
2026-04-05 | 0 | 4
2026-04-06 | 1 | 5
2026-04-07 | 0 | 5
2026-04-08 | 1 | 6
2026-04-09 | 1 | 7
```

without the ORDER BY, OVER () is every row that survives WHERE, so every row shows 7 here. with it, the window for each row stops at that row. april 6 is 5 because 2 + 0 + 1 + 1 + 0 + 1 = 5. the last row is 7, the plain total.

i assumed the sorting inside OVER was only for show, but it decides what "before" means. flip it to ORDER BY day DESC and april 1 shows 7 while april 9 shows 1.

the shops days never repeat, and that matters. rows that tie in the ORDER BY all show the same running value, one that counts all of them, and a later note digs into it.

### check yourself

1. this flips the order, and reads it through a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT used as a table). predict both rows.
```sql
SELECT day, running FROM (SELECT day, sum(placed) OVER (ORDER BY day DESC) AS running FROM daily_orders) AS t WHERE day IN (DATE '2026-04-01', DATE '2026-04-09') ORDER BY day
```
<details><summary>answer</summary>

```result
day | running
2026-04-01 | 7
2026-04-09 | 1
```
counting starts from april 9 now, so april 1 is last and has seen everything. the tempting answer is 2 and 7, from thinking DESC only reorders the display and changes nothing.

</details>

2. cancelled orders per day, april 4 has the only 1. what does the running total show on april 9?
```sql
SELECT day, sum(cancelled) OVER (ORDER BY day) AS running FROM daily_orders WHERE day = DATE '2026-04-09'
```
<details><summary>answer</summary>

```result
day | running
2026-04-09 | 0
```
a surprise: WHERE (keeps matching rows) runs before the window, so only april 9 is left to add up and the total is 0. with the filter outside, in a [subquery in FROM](./175-subquery-in-from.md), it is 1. the tempting answer is 1, from picturing the running total as already built.

</details>

---
prev: [188 RANK vs DENSE_RANK, what ties do](./188-rank-vs-dense-rank-what-ties-do.md) | next: not written yet
