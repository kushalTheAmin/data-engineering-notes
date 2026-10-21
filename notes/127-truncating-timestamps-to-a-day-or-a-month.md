# 127: truncating timestamps to a day or a month
builds on: [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [126 date parts, pulling out the year, month and day](./126-date-parts-pulling-out-the-year-month-and-day.md)
section: asking questions with SQL, part 27, ~2 min read

orders 101 and 102 both happened on April 1, but their ordered_at values are hours apart. so how does SQL see them as the same day?

[126](./126-date-parts-pulling-out-the-year-month-and-day.md) ended on a problem: its extract (pull one part out of a date) gives month 4 and forgets the year. `date_trunc('day', x)` is the fix: it chops a timestamp (a day plus a clock time) down to the start of its day, and `'month'` chops down to the first of the month.

the shop, the imaginary gujarati snack store these notes run on, has an orders [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). a slice of 4 of its 7 orders, with two [computed columns](./122-computed-columns-and-as.md) (calculations in SELECT):

| order_id | ordered_at | date_trunc day | date_trunc month |
|---|---|---|---|
| 101 | 2026-04-01 09:15:00 | 2026-04-01 00:00:00 | 2026-04-01 00:00:00 |
| 102 | 2026-04-01 18:40:00 | 2026-04-01 00:00:00 | 2026-04-01 00:00:00 |
| 103 | 2026-04-03 12:05:00 | 2026-04-03 00:00:00 | 2026-04-01 00:00:00 |
| 107 | 2026-04-09 13:45:00 | 2026-04-09 00:00:00 | 2026-04-01 00:00:00 |

101 and 102 now share a day value, and all four share one month value. unlike extract, that month value keeps the year, so March 2027 would be 2027-03-01, never equal to March 2026.

i assumed truncating made the clock part disappear. it doesnt, it gets set to midnight, so the result is still a timestamp. that matters in [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keep matching rows):

```sql
SELECT (SELECT count(*) FROM orders WHERE ordered_at = DATE '2026-04-01') AS plain, (SELECT count(*) FROM orders WHERE date_trunc('day', ordered_at) = DATE '2026-04-01') AS truncated
```

```result
plain | truncated
0 | 2
```

the date in the query, DATE '2026-04-01' (a calendar day, no clock), is read as midnight, so no order matches it exactly. no error, just zero. truncating first fixes it.

this is how daily and monthly reports decide which orders belong together. DuckDB (the database these notes run in) returns a timestamp even when you give date_trunc a date. Postgres, another database, has date_trunc too. a later note counts per day with it.

### check yourself

1. the shop has 7 orders, all in April 2026. what does this count, without running it?

```sql
SELECT count(*) AS n FROM orders WHERE date_trunc('month', ordered_at) = DATE '2026-04-01'
```
<details><summary>answer</summary>

```result
n
7
```

7, every order. truncating to the month sets each timestamp to 2026-04-01 00:00:00, and a plain date is read as that same midnight, so they match. the tempting answer is 0, from the trap above, but that failed only because the raw timestamp had a clock time.

</details>

2. a report counts orders by extract(month ...) across 2026 and 2027. switching to date_trunc('month', ...) changes what?
<details><summary>answer</summary>

March 2026 and March 2027 stop merging. extract gives 3 for both, date_trunc gives 2026-03-01 and 2027-03-01. the tempting answer is "nothing, both mean month", but only date_trunc keeps the year.

</details>

3. someone filters date_trunc('day', ordered_at) = TIMESTAMP '2026-04-01 09:15:00'. does order 101 match?
<details><summary>answer</summary>

no. truncating to the day sets the clock to 00:00:00, so the left side is 2026-04-01 00:00:00, never 09:15:00. the tempting yes assumes the clock survives.

</details>

---
prev: [126 date parts, pulling out the year, month and day](./126-date-parts-pulling-out-the-year-month-and-day.md) | next: not written yet
