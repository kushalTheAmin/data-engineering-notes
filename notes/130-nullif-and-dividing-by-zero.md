# 130: NULLIF and dividing by zero
builds on: [031 null, a marker for a missing value](./031-null.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md), [116 COALESCE, a fallback when a value is NULL](./116-coalesce-a-fallback-when-a-value-is-null.md), [122 computed columns and AS](./122-computed-columns-and-as.md)
section: asking questions with SQL, part 30, ~2 min read

a daily report divides cancelled orders by orders placed. april 5 had no orders at all. so what is 0 divided by 0?

NULLIF(a, b) hands back a, unless a equals b, and then it hands back [null](./031-null.md), a missing value. so NULLIF(placed, 0) turns a zero into null, and dividing by null just gives null. its the mirror of [COALESCE](./116-coalesce-a-fallback-when-a-value-is-null.md), which swaps a null for a fallback.

the shop, the imaginary gujarati snack store these notes run on, got a small [table](./079-a-table-rows-are-records-columns-are-fields.md) for this, daily_orders, one row per day. a slice, april 3 to 5, picked with [BETWEEN](./112-between-ranges-that-include-both-ends.md) (a range test, both ends included), with a [computed column](./122-computed-columns-and-as.md) (a calculation in SELECT) each way:

```sql
SELECT day, placed, cancelled, cancelled / placed AS raw_rate, cancelled / NULLIF(placed, 0) AS safe_rate FROM daily_orders WHERE day BETWEEN DATE '2026-04-03' AND DATE '2026-04-05' ORDER BY day
```

```result
day | placed | cancelled | raw_rate | safe_rate
2026-04-03 | 1 | 0 | 0.0 | 0.0
2026-04-04 | 1 | 1 | 1.0 | 1.0
2026-04-05 | 0 | 0 | nan | NULL
```

i expected a database to refuse, the way python raises ZeroDivisionError, and DuckDB, the database these notes run on, just carries on and hands back nan (not a number). the NULLIF column says NULL, which is the honest answer, there was no rate that day.

the nan is the dangerous one, it spreads into whatever uses it:

```sql
SELECT avg(cancelled / placed) AS raw_avg, round(avg(cancelled / NULLIF(placed, 0)), 2) AS safe_avg FROM daily_orders
```

```result
raw_avg | safe_avg
nan | 0.17
```

three zero days among the 9 turn the whole average into nan. with NULLIF avg, the average, skips those days and gets 1 over the 6 days that had orders.

Postgres doesnt return anything here, it raises a division_by_zero error and your query fails, so the guard is the same habit in both databases, just for different reasons. NULLIF lets you decide an empty day is NULL, instead of the database deciding.

---
prev: [129 the difference between two dates](./129-the-difference-between-two-dates.md) | next: not written yet
