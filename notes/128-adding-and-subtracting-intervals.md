# 128: adding and subtracting intervals
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [127 truncating timestamps to a day or a month](./127-truncating-timestamps-to-a-day-or-a-month.md)
section: asking questions with SQL, part 28, ~2 min read

what do you get for January 31 plus one month? there is no February 31, so the database has to pick something.

[127](./127-truncating-timestamps-to-a-day-or-a-month.md) chopped a timestamp (a day plus a clock time) down to its day. this one moves it. an interval is a length of time, like 2 days or 1 month, and adding it to a [date](./027-dates-and-times-apart.md) (a calendar day) or a timestamp gives a new moment. in python that is timedelta.

the shop, the imaginary gujarati snack store these notes run on, has an orders [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). say every order is due 2 days after it was placed. that is a [computed column](./122-computed-columns-and-as.md) (a calculation in SELECT, the part that picks what to show), on a slice of 4 of the 7 orders:

```sql
SELECT order_id, ordered_at, ordered_at + INTERVAL 2 DAY AS due_by FROM orders WHERE order_id IN (101, 102, 103, 107) ORDER BY order_id
```

```result
order_id | ordered_at | due_by
101 | 2026-04-01 09:15:00 | 2026-04-03 09:15:00
102 | 2026-04-01 18:40:00 | 2026-04-03 18:40:00
103 | 2026-04-03 12:05:00 | 2026-04-05 12:05:00
107 | 2026-04-09 13:45:00 | 2026-04-11 13:45:00
```

the clock part rides along untouched.

now the puzzle, with a plain date this time:

```sql
SELECT DATE '2026-01-31' + INTERVAL 1 MONTH AS plus_month, DATE '2026-01-31' + INTERVAL 30 DAY AS plus_30_days
```

```result
plus_month | plus_30_days
2026-02-28 00:00:00 | 2026-03-02 00:00:00
```

i assumed 1 month was just a nickname for 30 days. it isnt. it means the same day number next month, and when that day doesnt exist it lands on the last day of that month. a day count is exact, a month count is not. DuckDB also turns a date plus an interval into a timestamp, hence the 00:00:00.

this bites in real jobs, like "every month on the 31st", where the two readings differ. Postgres, another popular database, writes it with quotes, `INTERVAL '2 days'`, and DuckDB accepts that form too.

### check yourself

1. what does this return, without running it?

```sql
SELECT DATE '2026-03-31' + INTERVAL 1 MONTH AS d
```
<details><summary>answer</summary>

```result
d
2026-04-30 00:00:00
```

April has no 31st, so it lands on the last day, April 30. the tempting answer is May 1, from counting 31 days forward.

</details>

2. the report date is 2026-04-09 14:00. orders 104, 105, 106 and 107 came in at 04-04 08:30, 04-06 19:10, 04-08 10:00 and 04-09 13:45. how many were placed in the 3 days before the report?

```sql
SELECT count(*) AS n FROM orders WHERE ordered_at > TIMESTAMP '2026-04-09 14:00:00' - INTERVAL 3 DAY
```
<details><summary>answer</summary>

```result
n
3
```

the cutoff is April 6 at 14:00, so 105, 106 and 107 count, and 104 is too early. the tempting answer is 2, from reading it as "after April 6" and forgetting 105 came in that evening.

</details>

3. add one month to January 31, then subtract one month. do you get January 31 back?

```sql
SELECT (DATE '2026-01-31' + INTERVAL 1 MONTH) - INTERVAL 1 MONTH AS back
```
<details><summary>answer</summary>

```result
back
2026-01-28 00:00:00
```

no. the first step snaps down to February 28, and subtracting a month from that gives January 28. the tempting yes assumes adding and subtracting undo each other.

</details>

---
prev: [127 truncating timestamps to a day or a month](./127-truncating-timestamps-to-a-day-or-a-month.md) | next: [129 the difference between two dates](./129-the-difference-between-two-dates.md)
