# 198: date spines, a left join that keeps the empty days
builds on: [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [143 GROUP BY, one group per value](./143-group-by-one-group-per-value.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [160 the nulls a left join creates](./160-the-nulls-a-left-join-creates.md), [161 a WHERE that quietly turns a left join into an inner join](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md), [197 generate_series, a column of consecutive days](./197-generate-series-a-column-of-consecutive-days.md)
section: bigger queries, part 25, ~2 min read

group the shops orders by day and you get 6 rows. the shop traded for 9 days, april 2, 5 and 7 were just quiet, and a chart of those 6 rows would skip right over them. how do you get a row for a day with nothing in it?

a date spine is a column of every day you care about, with the data left joined onto it. the [generate_series](./197-generate-series-a-column-of-consecutive-days.md) days (9 rows made from nothing) go on the left, orders (order_id, ordered_at, status) on the right, so no day can fall out. the shop is the imaginary gujarati snack store these notes run on:

```sql
SELECT CAST(s.d AS DATE) AS day, count(o.order_id) AS orders FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS s(d) LEFT JOIN orders o ON CAST(o.ordered_at AS DATE) = CAST(s.d AS DATE) GROUP BY day ORDER BY day
```

```result
day | orders
2026-04-01 | 2
2026-04-02 | 0
2026-04-03 | 1
2026-04-04 | 1
2026-04-05 | 0
2026-04-06 | 1
2026-04-07 | 0
2026-04-08 | 1
2026-04-09 | 1
```

each spine day looks for orders on the same date, and [CAST](./132-cast-changing-a-values-type.md) turns the order timestamp into a plain day so they can match. april 2 finds nobody, so the [left join](./159-left-join-keep-every-row-from-the-left-table.md) (keeps every left row, matched or not) fills the order side with [NULL](./160-the-nulls-a-left-join-creates.md), a missing value. then [GROUP BY](./143-group-by-one-group-per-value.md) makes one row per day, and [count(o.order_id)](./138-count-star-vs-count-of-a-column.md) skips the NULL, so those days read 0. in python it is a dictionary of orders per day, read with counts.get(day, 0) for every day in a list of all days.

i expected the empty days to need a patch afterwards, but there is nothing to patch, the spine just refuses to lose them.

so what: an average per day over the grouped orders is 7 over 6 days, about 1.17. over the spine it is 7 over 9, about 0.78, and thats the honest one.

### check yourself

1. i swap count(o.order_id) for count(*). what does the april 5 row show, 0 or something else?
```sql
SELECT count(*) AS orders FROM generate_series(DATE '2026-04-05', DATE '2026-04-05', INTERVAL 1 DAY) AS s(d) LEFT JOIN orders o ON CAST(o.ordered_at AS DATE) = CAST(s.d AS DATE)
```
<details><summary>answer</summary>

```result
orders
1
```
1, not 0. the join made one filled-in row for that day and count(*) counts rows. the tempting answer is 0, from trusting that an empty day counts nothing.

</details>

2. i only want delivered orders, so i add WHERE (keeps only matching rows) o.status = 'delivered' to the first query. without running it, how many days come back?
```sql
SELECT CAST(s.d AS DATE) AS day, count(o.order_id) AS orders FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS s(d) LEFT JOIN orders o ON CAST(o.ordered_at AS DATE) = CAST(s.d AS DATE) WHERE o.status = 'delivered' GROUP BY day ORDER BY day
```
<details><summary>answer</summary>

```result
day | orders
2026-04-01 | 2
2026-04-03 | 1
2026-04-06 | 1
2026-04-09 | 1
```
4 days. the fix is to put the status test in the ON instead, which keeps all 9. the WHERE runs after the join, so the NULL status of an empty day fails it, and so do the cancelled april 4 and pending april 8. the tempting answer is 9, from thinking the spine protects the days even from a later filter ([161](./161-a-where-that-quietly-turns-a-left-join-into-an-inner-join.md)).

</details>

---
prev: [197 generate_series, a column of consecutive days](./197-generate-series-a-column-of-consecutive-days.md) | next: not written yet
