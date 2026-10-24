# 201: cohorts, the month each customer first showed up
builds on: [127 date_trunc](./127-truncating-timestamps-to-a-day-or-a-month.md), [132 CAST](./132-cast-changing-a-values-type.md), [138 count star](./138-count-star-vs-count-of-a-column.md), [142 min and max](./142-min-and-max-the-smallest-and-biggest-value.md), [143 GROUP BY](./143-group-by-one-group-per-value.md), [175 subquery in FROM](./175-subquery-in-from.md)
section: bigger queries, part 28, ~2 min read

Asha logged in during january, february and march. so which month did she join? you cant put her in three.

a cohort is a group of customers who first showed up in the same month, and a customers cohort month is the month of their earliest row. the shop, the imaginary gujarati snack store these notes run on, has a new logins table, one row per customer per login day. 8 rows go in, 5 customers come out:

| customer | login days (logins) | earliest | cohort |
|---|---|---|---|
| Asha | jan 5, feb 10, mar 2 | jan 5 | january |
| Bhavin | jan 20 | jan 20 | january |
| Chirag | feb 3, feb 25 | feb 3 | february |
| Disha | feb 14 | feb 14 | february |
| Esha | mar 8 | mar 8 | march |

[min](./142-min-and-max-the-smallest-and-biggest-value.md) (the earliest date) per [GROUP BY](./143-group-by-one-group-per-value.md) customer collapses the rows, and [date_trunc](./127-truncating-timestamps-to-a-day-or-a-month.md) (chop a date down to its month start) names the month. then a second GROUP BY counts customers per cohort, so the first step sits in a [subquery in FROM](./175-subquery-in-from.md) (an inner SELECT read like a table):

```sql
SELECT cohort, count(*) AS customers FROM (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id) AS t GROUP BY cohort ORDER BY cohort
```

```result
cohort | customers
2026-01-01 | 2
2026-02-01 | 2
2026-03-01 | 1
```

the trap is doing the month first. truncate every login and group by month, and Asha lands in all three cohorts, so the cohorts read 2, 3 and 2, and 5 people add up to 7. the min has to come first, one row per customer, then count.

i assumed a cohort would be a column somebody fills in, but nothing stores it. a customer has none until a query makes one, so a login that arrives late with an older date moves them to an earlier cohort.

the next one asks which of these customers came back the month after.

### check yourself

1. i skip the min, group by customer and month, then count per month. what does february show?
```sql
SELECT cohort, count(*) AS customers FROM (SELECT customer_id, CAST(date_trunc('month', login_on) AS DATE) AS cohort FROM logins GROUP BY customer_id, cohort) AS t GROUP BY cohort ORDER BY cohort
```
<details><summary>answer</summary>

```result
cohort | customers
2026-01-01 | 2
2026-02-01 | 3
2026-03-01 | 2
```
february shows 3, because Asha logged in that month too and gets counted again. the tempting answer is 2, from assuming a month count is a count of new people.

</details>

2. i swap min for max. which month is now the biggest cohort?
```sql
SELECT cohort, count(*) AS customers FROM (SELECT customer_id, CAST(date_trunc('month', max(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id) AS t GROUP BY cohort ORDER BY cohort
```
<details><summary>answer</summary>

```result
cohort | customers
2026-01-01 | 1
2026-02-01 | 2
2026-03-01 | 2
```
february and march tie at 2, since max puts Asha in march, her last month. the tempting answer is january, from thinking the biggest cohort stays put when only the function changes.

</details>

---
prev: [200 session ids, a running sum of the flags](./200-session-ids-a-running-sum-of-the-flags.md) | next: not written yet
