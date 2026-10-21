# 129: the difference between two dates
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [128 adding and subtracting intervals](./128-adding-and-subtracting-intervals.md)
section: asking questions with SQL, part 29, ~2 min read

order 102 came in on april 1 at 18:40 and order 103 on april 3 at 12:05. how many days apart are they? less than two full days passed, so is the answer 1 or 2?

in [128](./128-adding-and-subtracting-intervals.md) i moved a timestamp (a day plus a clock time) with an [interval](./128-adding-and-subtracting-intervals.md), a length of time. this goes the other way: subtract two moments and you get the gap between them. python does the same when you subtract two datetimes.

the shop, the imaginary gujarati snack store these notes run on, has an orders [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). here are orders 102 and 103 as a [computed column](./122-computed-columns-and-as.md) (a calculation in SELECT), two ways:

```sql
SELECT b.ordered_at - a.ordered_at AS gap, date_diff('day', a.ordered_at, b.ordered_at) AS day_diff FROM orders a, orders b WHERE a.order_id = 102 AND b.order_id = 103
```

```result
gap | day_diff
1 day, 17:25:00 | 2
```

the minus gives the real gap, 1 day and 17 hours 25 minutes. date_diff gives 2. i assumed it counted full days that passed, and it counts how many midnights you cross. april 2 and april 3 both start inside that window, so 2.

with plain [dates](./027-dates-and-times-apart.md) (calendar days, no clock) there is nothing to argue about:

```sql
SELECT DATE '2026-04-03' - DATE '2026-04-01' AS days
```

```result
days
2
```

for elapsed time, subtract the timestamps. if you want calendar days apart, like "how many days late is this", use date_diff or cast to dates first. months work the same way, so Jan 31 to Feb 1 is 1 month by date_diff.

this bites in reports like "orders delivered within 2 days", where the two readings disagree for a delivery two calendar days after the order, if it comes later in the day than the order did.

---
prev: [128 adding and subtracting intervals](./128-adding-and-subtracting-intervals.md) | next: [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md)
