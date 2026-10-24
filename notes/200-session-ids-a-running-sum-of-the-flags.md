# 200: session ids, a running sum of the flags
builds on: [180 CTEs](./180-ctes-naming-each-step-with-with.md), [186 PARTITION BY](./186-partition-by-a-separate-window-per-group.md), [189 running totals](./189-running-totals.md), [199 session starts](./199-session-starts-flag-the-click-after-a-long-gap.md)
section: bigger queries, part 27, ~2 min read

a column of 1s and 0s tells me where sessions start, but i want to say "these three clicks are session 1". how do you turn flags into numbers?

add them up as you go. a [running total](./189-running-totals.md) (a sum that grows down the rows) of the start flags goes up by 1 at every new session and stays put otherwise, so every click in a session shares one number. in the shop, the imaginary gujarati snack store these notes run on, [199](./199-session-starts-flag-the-click-after-a-long-gap.md) flagged the first click after 30 quiet minutes (new_session, 1 or 0) in clicks, where customer 1 is Asha and customer 2 is Bhavin. i name that step with a [CTE](./180-ctes-naming-each-step-with-with.md) (a query named up front with WITH) called flagged, because a window function cant sit inside another one:

```sql
WITH flagged AS (SELECT customer_id, clicked_at, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (PARTITION BY customer_id ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t) SELECT customer_id, clicked_at, new_session, sum(new_session) OVER (PARTITION BY customer_id ORDER BY clicked_at) AS session_id FROM flagged ORDER BY customer_id, clicked_at
```

```result
customer_id | clicked_at | new_session | session_id
1 | 2026-04-01 09:00:00 | 1 | 1
1 | 2026-04-01 09:05:00 | 0 | 1
1 | 2026-04-01 09:10:00 | 0 | 1
1 | 2026-04-01 11:00:00 | 1 | 2
1 | 2026-04-01 11:12:00 | 0 | 2
2 | 2026-04-01 09:02:00 | 1 | 1
2 | 2026-04-01 09:50:00 | 1 | 2
```

read Ashas rows top to bottom: 1, then two 0s add nothing, then the 1 at 11:00 makes it 2. i expected a session id to need some clever grouping step, but it is just the flag column added up.

the catch is [PARTITION BY](./186-partition-by-a-separate-window-per-group.md) customer_id (a separate window per group). it restarts the count, so Bhavin has a session 1 too. session_id alone isnt unique, the pair (customer_id, session_id) is.

so what: once every click has an id, a GROUP BY on that pair gives one row per session, with its start, end and click count.

### check yourself

1. i drop PARTITION BY from the sum, so it reads sum(new_session) OVER (ORDER BY clicked_at) over all 7 clicks. what session_id do Bhavins two clicks get?
```sql
WITH flagged AS (SELECT customer_id, clicked_at, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (PARTITION BY customer_id ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t) SELECT customer_id, clicked_at, sum(new_session) OVER (ORDER BY clicked_at) AS session_id FROM flagged ORDER BY customer_id, clicked_at
```
<details><summary>answer</summary>

```result
customer_id | clicked_at | session_id
1 | 2026-04-01 09:00:00 | 1
1 | 2026-04-01 09:05:00 | 2
1 | 2026-04-01 09:10:00 | 2
1 | 2026-04-01 11:00:00 | 4
1 | 2026-04-01 11:12:00 | 4
2 | 2026-04-01 09:02:00 | 2
2 | 2026-04-01 09:50:00 | 3
```
Bhavin gets 2 and 3, because Ashas 09:00 start is already counted when his 09:02 click arrives. the tempting answer is 1 and 2, from forgetting the sum now runs over everyones clicks in time order.

</details>

2. i keep PARTITION BY but delete the ORDER BY inside OVER, then keep only Asha. what do her 5 clicks show?
```sql
WITH flagged AS (SELECT customer_id, clicked_at, CASE WHEN gap IS NULL OR gap > 30 THEN 1 ELSE 0 END AS new_session FROM (SELECT customer_id, clicked_at, date_diff('minute', lag(clicked_at) OVER (PARTITION BY customer_id ORDER BY clicked_at), clicked_at) AS gap FROM clicks) AS t) SELECT customer_id, clicked_at, sum(new_session) OVER (PARTITION BY customer_id) AS session_id FROM flagged WHERE customer_id = 1 ORDER BY clicked_at
```
<details><summary>answer</summary>

```result
customer_id | clicked_at | session_id
1 | 2026-04-01 09:00:00 | 2
1 | 2026-04-01 09:05:00 | 2
1 | 2026-04-01 09:10:00 | 2
1 | 2026-04-01 11:00:00 | 2
1 | 2026-04-01 11:12:00 | 2
```
every row shows 2, the total number of sessions Asha had, because without ORDER BY the window is all her rows. the tempting answer is 1, 1, 1, 2, 2, from assuming the sum still counts in click order.

</details>

---
prev: [199 session starts, flagging the click after a long gap](./199-session-starts-flag-the-click-after-a-long-gap.md) | next: not written yet
