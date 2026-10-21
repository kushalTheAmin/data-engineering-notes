# 126: date parts, pulling out the year, month and day
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [079 a table, rows are records, columns are fields](./079-a-table-rows-are-records-columns-are-fields.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [122 computed columns and AS](./122-computed-columns-and-as.md), [125 concatenating text, and taking pieces of it](./125-concatenating-text-and-taking-pieces-of-it.md)
section: asking questions with SQL, part 26, ~2 min read

your boss asks for "orders by month". the column holds 2026-04-09 13:45:00, so where is the month? if you were hoping for the word April, it isnt coming.

[125](./125-concatenating-text-and-taking-pieces-of-it.md) cut pieces out of text, this cuts pieces out of a [date](./027-dates-and-times-apart.md) (a calendar day) or a timestamp (a day plus a clock time). `extract(part FROM value)` returns one date part as a plain number, inside a [computed column](./122-computed-columns-and-as.md) (a calculation in SELECT). in python it is `dt.year`, `dt.month`, `dt.day`.

the shop, the imaginary gujarati snack store these notes run on, has an orders [table](./079-a-table-rows-are-records-columns-are-fields.md) (a grid of rows). a slice of 4 orders:

```sql
SELECT order_id, ordered_at, extract(year FROM ordered_at) AS yr, extract(month FROM ordered_at) AS mo, extract(day FROM ordered_at) AS dy FROM orders WHERE order_id IN (101, 103, 105, 107) ORDER BY order_id
```

```result
order_id | ordered_at | yr | mo | dy
101 | 2026-04-01 09:15:00 | 2026 | 4 | 1
103 | 2026-04-03 12:05:00 | 2026 | 4 | 3
105 | 2026-04-06 19:10:00 | 2026 | 4 | 6
107 | 2026-04-09 13:45:00 | 2026 | 4 | 9
```

i expected April, and the month is just 4, a whole number with no leading zero. that is useful though, because numbers filter easily. [WHERE](./106-where-keeping-only-the-rows-that-match.md) (keep matching rows) can use a date part, here on the customers joined_on date:

```sql
SELECT name, joined_on FROM customers WHERE extract(month FROM joined_on) = 3 ORDER BY customer_id
```

```result
name | joined_on
Disha | 2026-03-02
Esha | 2026-03-15
```

the catch is that month alone forgets the year. March 2026 and March 2027 both give 3, so a report grouped by month number over two years quietly mixes them. the shop only has 2026 so far, which hides it.

DuckDB and Postgres both take `extract(month FROM x)`. DuckDB also has short forms like `month(x)`.

---
prev: [125 concatenating text, and taking pieces of it](./125-concatenating-text-and-taking-pieces-of-it.md) | next: [127 truncating timestamps to a day or a month](./127-truncating-timestamps-to-a-day-or-a-month.md)
