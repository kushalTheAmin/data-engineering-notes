# 026: seconds, milliseconds, microseconds: one moment, three numbers
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md)
section: data at the atom level, part 26, ~2 min read

one api (how one program asks another for data) sends order 101 as 1775049300 and another sends 1775049300000. same order, so which is wrong? neither, but mixing them up is how orders end up dated January 1970.

seconds, milliseconds (thousandths of a second) and microseconds (millionths) are three units for the same count, [unix time](./025-unix-time.md), a moment kept as time since 1970 UTC. the shop, the imaginary gujarati snack store these notes run on, has order 101 at 09:15 on 1 April 2026, which i read as New York time like 025 did, so 13:15 in [UTC](./024-utc.md), the clock everyone measures against.

| unit | count since 1 Jan 1970 | digits |
|---|---|---|
| seconds | 1775049300 | 10 |
| milliseconds | 1775049300000 | 13 |
| microseconds | 1775049300000000 | 16 |

each row is the one above times 1000, and nothing else changes. same starting line, same moment. i expected the number to carry its unit somewhere, but its just digits, so you have to know which unit you are holding. for dates between 2001 and 2286, 10 digits means seconds and 13 means milliseconds.

now read each count with the wrong unit:

```python
from datetime import datetime, timezone

s = 1775049300
print(datetime.fromtimestamp(s / 1000, timezone.utc))
try:
    datetime.fromtimestamp(s * 1000, timezone.utc)
except ValueError as e:
    print(e)
```

```output
1970-01-21 13:04:09.300000+00:00
year 58219 is out of range
```

seconds read as milliseconds land 20 days after the start. milliseconds read as seconds point at the year 58219, which python refuses to show.

so what: JavaScript Date.now() gives milliseconds (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now) and Postgres, a popular server database, stores timestamps down to 1 microsecond (https://www.postgresql.org/docs/current/datatype-datetime.html). a busy shop can get several orders inside one second, and whole seconds cant order them well.

### check yourself

1. order 101 is at 09:15:00 and order 102 at 18:40:00 on 1 April, both on the same clock. predict the gap between their milliseconds counts.
```sql
SELECT max(epoch_ms(ordered_at)) - min(epoch_ms(ordered_at)) AS diff_ms FROM orders WHERE order_id IN (101, 102);
```
<details><summary>answer</summary>

```result
diff_ms
33900000
```
the gap is 9 hours 25 minutes, 33900 seconds, times 1000. the tempting answer is 33900, which is the gap in seconds.

</details>

2. a dashboard shows every new order dated around 21 January 1970. which was read as which: seconds as milliseconds, or the other way?
<details><summary>answer</summary>

seconds read as milliseconds. a 10 digit count is about 1.8 billion, and as milliseconds that is only about 20 days. the tempting answer is the other way round, but that gives a date tens of thousands of years away, not 1970.

</details>

---
prev: [025 unix time, counting seconds from 1970](./025-unix-time.md) | next: [027 dates without times, and times without dates](./027-dates-and-times-apart.md)
