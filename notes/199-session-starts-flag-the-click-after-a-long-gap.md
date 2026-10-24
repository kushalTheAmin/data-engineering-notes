# 199: session starts, flagging the click after a long gap
builds on: [031 NULL](./031-null.md), [123 CASE WHEN](./123-case-when-if-and-else-inside-a-query.md), [129 the difference between two dates](./129-the-difference-between-two-dates.md), [175 subquery in FROM](./175-subquery-in-from.md), [186 PARTITION BY](./186-partition-by-a-separate-window-per-group.md), [192 LAG and LEAD](./192-lag-and-lead-looking-at-the-row-before.md)
section: bigger queries, part 26, ~2 min read

a list of clicks has no sessions in it, just timestamps. so how does anyone say "this visit started here"?

a session is a run of clicks by one person, and a long enough silence starts a new one. so the first click after a long gap gets a flag of 1. the shop, the imaginary gujarati snack store these notes run on, now has a clicks table (one row per page view: customer_id, clicked_at, page), where customer 1 is Asha and customer 2 is Bhavin. i call 30 minutes of quiet a new session:

```sql
SELECT customer_id, clicked_at, gap, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (PARTITION BY customer_id ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t ORDER BY customer_id, clicked_at
```

```result
customer_id | clicked_at | gap | new_session
1 | 2026-04-01 09:00:00 | NULL | 1
1 | 2026-04-01 09:05:00 | 5 | 0
1 | 2026-04-01 09:10:00 | 5 | 0
1 | 2026-04-01 11:00:00 | 110 | 1
1 | 2026-04-01 11:12:00 | 12 | 0
2 | 2026-04-01 09:02:00 | NULL | 1
2 | 2026-04-01 09:50:00 | 48 | 1
```

[LAG](./192-lag-and-lead-looking-at-the-row-before.md) (the value from the row before) hands each click the previous click time, [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) customer_id (a separate window per group) keeps Asha and Bhavin apart, and [date_diff](./129-the-difference-between-two-dates.md) counts the minute marks crossed, exact here, every click sits on a whole minute. the gap is built in a [subquery in FROM](./175-subquery-in-from.md) (a query as a table) so the outer [CASE WHEN](./123-case-when-if-and-else-inside-a-query.md) (if/else inside a query) can read it by name.

the gotcha: a first click has a [NULL](./031-null.md) (missing value) gap, and NULL > 30 is unknown, not true, so without the IS NULL test the CASE says 0 and the first session never opens. i kept reading the flags as "big gap", but a first click is a start too.

Asha has 2 sessions, Bhavin 2, since 48 is over 30. exactly 30 stays in.

so what: you will see it, Google Analytics also ends a session after 30 minutes of inactivity by default.

### check yourself

1. i change the rule to gap > 60. how many clicks are flagged 1, and which flag flips?
<details><summary>answer</summary>

three clicks are flagged. Bhavin 09:50 flips to 0, because 48 is under 60. the tempting answer is 1, from forgetting that each first click opens a session too.

</details>

2. i delete PARTITION BY customer_id and keep only Bhavin with an outer WHERE. what do his two clicks show?
```sql
SELECT customer_id, clicked_at, gap, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t WHERE customer_id = 2 ORDER BY clicked_at
```
<details><summary>answer</summary>

```result
customer_id | clicked_at | gap | new_session
2 | 2026-04-01 09:02:00 | 2 | 0
2 | 2026-04-01 09:50:00 | 40 | 1
```
his first click now looks 2 minutes after ashas 09:00 click, so it opens no session, and his 09:50 looks 40 minutes after ashas 09:10 click. the tempting answer is NULL and 1, from forgetting that LAG sees everyones clicks.

</details>

---
prev: [198 date spines, a left join that keeps the empty days](./198-date-spines-a-left-join-that-keeps-the-empty-days.md) | next: [200 session ids, a running sum of the flags](./200-session-ids-a-running-sum-of-the-flags.md)
