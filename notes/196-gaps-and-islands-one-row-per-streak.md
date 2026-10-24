# 196: gaps and islands, one row per streak
builds on: [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [142 min and max, the smallest and biggest value](./142-min-and-max-the-smallest-and-biggest-value.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [175 subquery in FROM](./175-subquery-in-from.md), [195 gaps and islands, date minus row number](./195-gaps-and-islands-date-minus-row-number.md)
section: bigger queries, part 23, ~2 min read

so every day has a label now, but nobody wants 6 rows of labels, they want "the shop had a 2 day streak from april 3 to april 4". one more step gets there.

the label from [195](./195-gaps-and-islands-date-minus-row-number.md) is the same for every day in a streak, so it is a perfect key for [GROUP BY](./143-group-by-one-group-per-value.md) (one group per different value). then [min and max](./142-min-and-max-the-smallest-and-biggest-value.md) give the first and last day, and [count(*)](./138-count-star-vs-count-of-a-column.md) (counts every row) gives the length. the shop, the imaginary snack store these notes run on, has daily_orders, and 195 labeled its 6 order days:

```text
day         label        |  group by label  | first_day   last_day    days
2026-04-01  2026-03-31   |  2026-03-31      | 2026-04-01  2026-04-01  1
2026-04-03  2026-04-01   |  2026-04-01      | 2026-04-03  2026-04-04  2
2026-04-04  2026-04-01   |  2026-04-02      | 2026-04-06  2026-04-06  1
2026-04-06  2026-04-02   |  2026-04-03      | 2026-04-08  2026-04-09  2
2026-04-08  2026-04-03   |
2026-04-09  2026-04-03   |
```

6 rows in, 4 streaks out. the label is the loop key, like a dictionary of buckets filled by day. i put the labeling in a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT read like a table), because GROUP BY needs the label to already exist:

```sql
SELECT min(day) AS first_day, max(day) AS last_day, count(*) AS days FROM (SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders WHERE placed > 0) AS t GROUP BY label ORDER BY first_day
```

```result
first_day | last_day | days
2026-04-01 | 2026-04-01 | 1
2026-04-03 | 2026-04-04 | 2
2026-04-06 | 2026-04-06 | 1
2026-04-08 | 2026-04-09 | 2
```

the label itself isnt in the output, its only scaffolding, and thats what i found odd, a column you build just to throw away.

swap ORDER BY for days DESC and you can pull the longest streak, and it works the same on 900 days as on 9. it still needs one row per day, same catch as 195.

### check yourself

1. predict the span (last_day minus first_day) and days for the april 3 streak. are they equal?
```sql
SELECT min(day) AS first_day, max(day) - min(day) AS span, count(*) AS days FROM (SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders WHERE placed > 0) AS t GROUP BY label ORDER BY first_day
```
<details><summary>answer</summary>

```result
first_day | span | days
2026-04-01 | 0 | 1
2026-04-03 | 1 | 2
2026-04-06 | 0 | 1
2026-04-08 | 1 | 2
```
span 1, days 2. a streak of n days has a span of n minus 1, because the span counts the steps between days. the tempting answer is equal, from thinking the span counts days.

</details>

2. a teammate writes GROUP BY day instead of GROUP BY label. how many rows come back?
```sql
SELECT count(*) AS streaks FROM (SELECT day FROM (SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders WHERE placed > 0) AS t GROUP BY day)
```
<details><summary>answer</summary>

```result
streaks
6
```
6, one per day, each with days = 1. every date is different, so every day is its own group and no streak ever forms. the tempting answer is 4, from thinking the label is still doing the grouping.

</details>

---
prev: [195 gaps and islands, date minus row number](./195-gaps-and-islands-date-minus-row-number.md) | next: not written yet
