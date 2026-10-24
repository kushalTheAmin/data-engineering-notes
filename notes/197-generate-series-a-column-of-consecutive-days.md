# 197: generate_series, a column of consecutive days
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [128 adding and subtracting intervals](./128-adding-and-subtracting-intervals.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [158 table aliases, short nicknames for tables](./158-table-aliases-short-nicknames-for-tables.md), [179 NOT IN and the NULL trap](./179-not-in-and-the-null-trap.md), [195 gaps and islands, date minus row number](./195-gaps-and-islands-date-minus-row-number.md)
section: bigger queries, part 24, ~2 min read

the shop has an orders table with 7 rows but only 6 different days, so april 2, 5 and 7 have no row at all. [195](./195-gaps-and-islands-date-minus-row-number.md) needed one row per day and daily_orders had them ready, but a table like orders wont, so where do the rows come from?

generate_series(start, stop, step) makes rows out of nothing, one per step from start to stop, and the stop day is in when a step lands on it. you put it in FROM, where the rows come from. the shop, the imaginary gujarati snack store these notes run on, traded april 1 to 9:

```sql
SELECT CAST(d AS DATE) AS day FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS t(d)
```

```result
day
2026-04-01
2026-04-02
2026-04-03
2026-04-04
2026-04-05
2026-04-06
2026-04-07
2026-04-08
2026-04-09
```

the step is an [interval](./128-adding-and-subtracting-intervals.md) (a length of time, like 1 day). DuckDB, the database these notes run on, hands back timestamps (a day plus a clock time), so i [CAST](./132-cast-changing-a-values-type.md) them back to a [date](./027-dates-and-times-apart.md) (a calendar day). t(d) is a [table alias](./158-table-aliases-short-nicknames-for-tables.md) naming the [table](./079-a-table-rows-are-records-columns-are-fields.md) t and its column d.

the python version is a loop:

```python
from datetime import date, timedelta
days = []
day = date(2026, 4, 1)
while day <= date(2026, 4, 9):
    days.append(day)
    day += timedelta(days=1)
print(len(days), days[0], days[-1])
```

```output
9 2026-04-01 2026-04-09
```

i figured every row had to come from a table somewhere, and this one comes out of three values i typed. with a positive step, a start after the stop gives zero rows, not an error. DuckDB also has range(), the same thing but it skips the stop day, like python range.

Postgres has generate_series too too, with the interval spelled a little differently, so this exact query is DuckDB. the next one lines these 9 days up against orders.

### check yourself

1. predict the last day this returns, and how many rows.
```sql
SELECT CAST(d AS DATE) AS day FROM generate_series(DATE '2026-04-02', DATE '2026-04-09', INTERVAL 2 DAY) AS t(d)
```
<details><summary>answer</summary>

```result
day
2026-04-02
2026-04-04
2026-04-06
2026-04-08
```
4 rows, last day april 8. the stop is only in when a step lands on it, and 2, 4, 6, 8 jump over the 9th. the tempting answer is april 9, from reading stop as always included.

</details>

2. 9 days minus 7 orders is 2, so how many of the 9 days have no order? the orders fall on april 1 (two of them), 3, 4, 6, 8 and 9. [NOT IN](./179-not-in-and-the-null-trap.md) keeps values missing from a list.
```sql
SELECT count(*) AS empty_days FROM generate_series(DATE '2026-04-01', DATE '2026-04-09', INTERVAL 1 DAY) AS t(d) WHERE CAST(d AS DATE) NOT IN (SELECT CAST(ordered_at AS DATE) FROM orders)
```
<details><summary>answer</summary>

```result
empty_days
3
```
3 (april 2, 5 and 7). 7 orders cover only 6 days because april 1 has two orders. the tempting answer is 2, from subtracting orders from days as if each order took its own day.

</details>

---
prev: [196 gaps and islands, one row per streak](./196-gaps-and-islands-one-row-per-streak.md) | next: not written yet
