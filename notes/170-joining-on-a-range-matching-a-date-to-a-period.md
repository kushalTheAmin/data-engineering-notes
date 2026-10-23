# 170: joining on a range, matching a date to a period
builds on: [112 BETWEEN, ranges that include both ends](./112-between-ranges-that-include-both-ends.md), [132 CAST, changing a values type](./132-cast-changing-a-values-type.md), [157 ON, how a join decides which rows match](./157-on-how-a-join-decides-which-rows-match.md), [159 left join, keep every row from the left table](./159-left-join-keep-every-row-from-the-left-table.md), [164 fan out, when a join multiplies rows](./164-fan-out-when-a-join-multiplies-rows.md), [169 cross join, every row with every row](./169-cross-join-every-row-with-every-row.md)
section: combining tables with joins, part 16, ~2 min read

order 103 was placed on the last day of the launch week promo, and my join said it was in no promo at all. can you spot why?

a range join is a join whose [ON](./157-on-how-a-join-decides-which-rows-match.md) (the test that decides which pairs stay) is a [BETWEEN](./112-between-ranges-that-include-both-ends.md) instead of an equals. [157](./157-on-how-a-join-decides-which-rows-match.md) said ON takes any test, and this is that. the shop (the imaginary gujarati snack store these notes run on) now has promo_periods, a small table with a first and last day for each promo: launch week runs 2026-04-01 to 2026-04-03 and festival sale runs 2026-04-05 to 2026-04-07, and thats all of it. the join:

```sql
SELECT o.order_id, p.promo FROM orders o JOIN promo_periods p ON o.ordered_at BETWEEN p.starts_on AND p.ends_on ORDER BY o.order_id
```

```result
order_id | promo
101 | launch week
102 | launch week
105 | festival sale
```

order 103 is gone. its ordered_at is 2026-04-03 12:05, a timestamp (a date plus a time), and launch week ends on the date 2026-04-03, which counts as midnight. noon is after midnight, so the BETWEEN says no. the fix is to [CAST](./132-cast-changing-a-values-type.md) (convert) the timestamp to a date first, and a [left join](./159-left-join-keep-every-row-from-the-left-table.md) keeps the orders that match no promo, with NULL (a missing value) in the promo column:

```sql
SELECT o.order_id, p.promo FROM orders o LEFT JOIN promo_periods p ON CAST(o.ordered_at AS DATE) BETWEEN p.starts_on AND p.ends_on ORDER BY o.order_id
```

```result
order_id | promo
101 | launch week
102 | launch week
103 | launch week
104 | NULL
105 | festival sale
106 | NULL
107 | NULL
```

7 orders in, 7 rows out. 104 fell on april 4, between the two promos, and 106 and 107 came after both. one more thing to watch: if two periods overlap, an order inside both matches twice, and thats the [fan out](./164-fan-out-when-a-join-multiplies-rows.md) again. i kept picturing a join as matching ids, and a range join is really the cross join loop from [169](./169-cross-join-every-row-with-every-row.md) with a range check as the if.

---
prev: [169 cross join, every row with every row](./169-cross-join-every-row-with-every-row.md) | next: [171 joins plus GROUP BY, revenue per customer](./171-joins-plus-group-by-revenue-per-customer.md)
