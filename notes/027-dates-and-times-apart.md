# 027: dates without times, and times without dates
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md)
section: data at the atom level, part 27, ~2 min read

how many orders did the shop, the imaginary gujarati snack store these notes run on, get on or before 1 April? orders 101 and 102 are both on 1 April, so 2. i asked the database the obvious way and it said 0.

a date is a calendar day with nothing else, like Ashas joined_on, 2026-01-05. a time is a clock reading with no day, like 09:15:00. a timestamp, the full moment from [025](./025-unix-time.md), is both glued together. the casting operator :: converts a value to another type, so one timestamp splits into its two halves (a slice of 3 orders):

```sql
SELECT order_id, ordered_at::DATE AS day, ordered_at::TIME AS clock FROM orders WHERE order_id IN (101, 102, 103);
```

```result
order_id | day | clock
101 | 2026-04-01 | 09:15:00
102 | 2026-04-01 | 18:40:00
103 | 2026-04-03 | 12:05:00
```

now the bug. WHERE keeps only rows that match, and here i compare a timestamp to a date:

```sql
SELECT count(*) AS n FROM orders WHERE ordered_at <= DATE '2026-04-01';
```

```result
n
0
```

```sql
SELECT count(*) AS n FROM orders WHERE ordered_at::DATE <= DATE '2026-04-01';
```

```result
n
2
```

i assumed a date was a timestamp with the time hidden, but a date has no time at all. to compare, the database turns 2026-04-01 into midnight, 00:00:00, and 09:15 is after midnight, so both orders miss. casting the timestamp down to a date first fixes it.

so what: this is the classic end-of-month bug, a report for "up to 30 April" that quietly drops everything ordered on the 30th. one more caveat, neither type says which zones clock decided the day, and [024](./024-utc.md) already showed one moment can be two days, so you still need to know the clock.

---
prev: [026 seconds, milliseconds, microseconds](./026-seconds-milliseconds-microseconds.md) | next: not written yet
