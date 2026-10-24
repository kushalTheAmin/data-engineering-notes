# 195: gaps and islands, date minus row number
builds on: [027 dates without times, and times without dates](./027-dates-and-times-apart.md), [106 WHERE, keeping only the rows that match](./106-where-keeping-only-the-rows-that-match.md), [130 NULLIF and dividing by zero](./130-nullif-and-dividing-by-zero.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [187 ROW_NUMBER, numbering rows in order](./187-row-number-numbering-rows-in-order.md), [194 removing duplicates with ROW_NUMBER](./194-removing-duplicates-with-row-number.md)
section: bigger queries, part 22, ~2 min read

which days in a row did the shop get an order? you can eyeball 9 days, but 900 needs a trick: subtracting a counter from a date.

a run of consecutive days is an island, the empty days between are gaps, and the puzzle is called gaps and islands. in [194](./194-removing-duplicates-with-row-number.md) [ROW_NUMBER](./187-row-number-numbering-rows-in-order.md) (numbers rows 1, 2, 3) picked a winner, here it is a counter i subtract.

the shop, the imaginary snack store these notes run on, has daily_orders from [130](./130-nullif-and-dividing-by-zero.md), one row per day. take the days with at least one order, number them, and subtract that many days from each [date](./027-dates-and-times-apart.md) (a calendar day):

```python
from datetime import date, timedelta
days = [date(2026, 4, 1), date(2026, 4, 3), date(2026, 4, 4), date(2026, 4, 6), date(2026, 4, 8), date(2026, 4, 9)]
for n, d in enumerate(days, start=1):
    print(n, d, d - timedelta(days=n))
```

```output
1 2026-04-01 2026-03-31
2 2026-04-03 2026-04-01
3 2026-04-04 2026-04-01
4 2026-04-06 2026-04-02
5 2026-04-08 2026-04-03
6 2026-04-09 2026-04-03
```

april 3 and 4 share a label, so do april 8 and 9. inside an island the date goes up by 1 and the counter goes up by 1, so the difference stands still. at a gap the date jumps by 2 or more but the counter only by 1, so the label changes. same label, same island. i kept looking for a comparison between neighbors, and there isnt one.

the same in SQL, with the date minus the counter called label. 4 different labels means 4 islands from 6 days:

```sql
SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders WHERE placed > 0 ORDER BY day
```

```result
day | label
2026-04-01 | 2026-03-31
2026-04-03 | 2026-04-01
2026-04-04 | 2026-04-01
2026-04-06 | 2026-04-02
2026-04-08 | 2026-04-03
2026-04-09 | 2026-04-03
```

[WHERE](./106-where-keeping-only-the-rows-that-match.md) (keeps matching rows) runs before the numbering, so only days with orders get counted. OVER (ORDER BY day) numbers in date order. DuckDB wants an INTEGER here, hence the [CAST](./132-cast-changing-a-values-type.md) (converts a type).

the catch is one row per day, because a day listed twice bumps the counter without moving the date.

### check yourself

1. number all 9 days with no WHERE. DISTINCT keeps one copy of identical rows. how many different labels come back?
```sql
SELECT DISTINCT day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM daily_orders
```
<details><summary>answer</summary>

```result
label
2026-03-31
```
1 label. the empty days get numbered too, so the counter keeps pace with the date and the gaps vanish. the tempting answer is 4, from thinking the labels come from the data alone.

</details>

2. a feed lists april 4 twice by mistake, and UNION ALL stacks two results. what label does april 6 get, and which island does it wrongly join?
```sql
SELECT day, day - CAST(row_number() OVER (ORDER BY day) AS INTEGER) AS label FROM (SELECT day FROM daily_orders WHERE placed > 0 UNION ALL SELECT DATE '2026-04-04') AS t ORDER BY day, label
```
<details><summary>answer</summary>

```result
day | label
2026-04-01 | 2026-03-31
2026-04-03 | 2026-04-01
2026-04-04 | 2026-03-31
2026-04-04 | 2026-04-01
2026-04-06 | 2026-04-01
2026-04-08 | 2026-04-02
2026-04-09 | 2026-04-02
```
april 6 gets 2026-04-01, the label of april 3 and one april 4, so it looks like part of that island, and the extra april 4 row lands with april 1. the extra row pushed every later counter up by 1. the tempting answer is that only the duplicate goes wrong.

</details>

---
prev: [194 removing duplicates with ROW_NUMBER](./194-removing-duplicates-with-row-number.md) | next: [196 gaps and islands, one row per streak](./196-gaps-and-islands-one-row-per-streak.md)
