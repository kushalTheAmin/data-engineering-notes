# 202: retention, who came back the month after
builds on: [121 DISTINCT](./121-distinct-removing-duplicate-rows.md), [127 date_trunc](./127-truncating-timestamps-to-a-day-or-a-month.md), [128 intervals](./128-adding-and-subtracting-intervals.md), [138 count star vs count of a column](./138-count-star-vs-count-of-a-column.md), [159 left join](./159-left-join-keep-every-row-from-the-left-table.md), [180 CTEs](./180-ctes-naming-each-step-with-with.md), [201 cohorts](./201-cohorts-the-month-each-customer-first-showed-up.md)
section: bigger queries, part 29, ~2 min read

asha came back the month after she joined and bhavin never did. how do you turn that into a count per cohort?

retention is how many people from a [cohort](./201-cohorts-the-month-each-customer-first-showed-up.md) (customers whose first login was in the same month, not their signup month) logged in again, here in the month right after their first. the shop, the imaginary gujarati snack store these notes run on, keeps its site logins in a logins table. first each customers story:

| customer | cohort | months with a login | back the month after? |
|---|---|---|---|
| Asha | january | jan, feb, mar | yes, february |
| Bhavin | january | jan | no |
| Chirag | february | feb | no |
| Disha | february | feb | no |
| Esha | march | mar | no |

i need two lists, so two [CTEs](./180-ctes-naming-each-step-with-with.md) (queries named up front with WITH): cohorts, each customers first month from 201, and active, every month each customer logged in. then [left join](./159-left-join-keep-every-row-from-the-left-table.md) active onto cohorts, matching the same customer and the month equal to the cohort plus one [month](./128-adding-and-subtracting-intervals.md):

```sql
WITH cohorts AS (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id), active AS (SELECT DISTINCT customer_id, CAST(date_trunc('month', login_on) AS DATE) AS active_month FROM logins) SELECT c.cohort, count(*) AS customers, count(a.customer_id) AS came_back FROM cohorts AS c LEFT JOIN active AS a ON a.customer_id = c.customer_id AND a.active_month = c.cohort + INTERVAL 1 MONTH GROUP BY c.cohort ORDER BY c.cohort
```

```result
cohort | customers | came_back
2026-01-01 | 2 | 1
2026-02-01 | 2 | 0
2026-03-01 | 1 | 0
```

a customer who never came back is a left join row with nothing next to it, and [count of a column](./138-count-star-vs-count-of-a-column.md) skips that empty spot, a NULL. i kept expecting retention to need its own feature, but the join already remembers who is missing. [DISTINCT](./121-distinct-removing-duplicate-rows.md) (keep one copy of repeated rows) in active gives one row per customer per month, so two logins in a month cant match twice.

so what: march shows 0, but the logins stop in march, so that 0 means april isnt in the data yet, not that nobody came back. always check the newest cohort before trusting its number.

### check yourself

1. i change the LEFT JOIN to INNER JOIN (keeps only matched rows). how many cohort rows come back, and what does january say?
```sql
WITH cohorts AS (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id), active AS (SELECT DISTINCT customer_id, CAST(date_trunc('month', login_on) AS DATE) AS active_month FROM logins) SELECT c.cohort, count(*) AS customers, count(a.customer_id) AS came_back FROM cohorts AS c INNER JOIN active AS a ON a.customer_id = c.customer_id AND a.active_month = c.cohort + INTERVAL 1 MONTH GROUP BY c.cohort ORDER BY c.cohort
```
<details><summary>answer</summary>

```result
cohort | customers | came_back
2026-01-01 | 1 | 1
```
one row, and january claims 1 customer, so Bhavin vanished from the cohort size and retention looks like 100%. the tempting answer is the same 3 rows, from thinking the join type only changes the matches.

</details>

2. Chirag logged in twice in february. i drop DISTINCT from active and match the cohort month itself instead of the month after. how many customers does february show?
```sql
WITH cohorts AS (SELECT customer_id, CAST(date_trunc('month', min(login_on)) AS DATE) AS cohort FROM logins GROUP BY customer_id), active AS (SELECT customer_id, CAST(date_trunc('month', login_on) AS DATE) AS active_month FROM logins) SELECT c.cohort, count(*) AS customers, count(a.customer_id) AS came_back FROM cohorts AS c LEFT JOIN active AS a ON a.customer_id = c.customer_id AND a.active_month = c.cohort GROUP BY c.cohort ORDER BY c.cohort
```
<details><summary>answer</summary>

```result
cohort | customers | came_back
2026-01-01 | 2 | 2
2026-02-01 | 3 | 3
2026-03-01 | 1 | 1
```
3, because Chirag logged in twice in february, so he matches two rows and count(*) counts both. the tempting answer is 2, from counting people and not matched rows.

</details>

---
prev: [201 cohorts, the month each customer first showed up](./201-cohorts-the-month-each-customer-first-showed-up.md) | next: not written yet
