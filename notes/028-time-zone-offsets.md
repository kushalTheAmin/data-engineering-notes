# 028: time zones, offsets from UTC
builds on: [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md), [027 dates without times, and times without dates](./027-dates-and-times-apart.md)
section: data at the atom level, part 28, ~2 min read

[027](./027-dates-and-times-apart.md) ended on a loose thread: a date or a time never says which clock decided it. so how do you write a time that does say? the shop, the imaginary gujarati snack store these notes run on, has order 101 at 09:15 on 1 April.

an offset is the number of hours and minutes a clock sits ahead of or behind [UTC](./024-utc.md), the one reference clock. you write it right after the time, like -04:00, and now the text carries its own clock. here is order 101 three ways, then the python check:

```python
from datetime import datetime

for s in ["2026-04-01T09:15:00-04:00", "2026-04-01T18:45:00+05:30", "2026-04-01T13:15:00Z"]:
    print(s, int(datetime.fromisoformat(s).timestamp()))
```

```output
2026-04-01T09:15:00-04:00 1775049300
2026-04-01T18:45:00+05:30 1775049300
2026-04-01T13:15:00Z 1775049300
```

three different clock readings, one [unix time](./025-unix-time.md) count, so one moment. to get UTC, undo the offset: 09:15 minus -4 hours is 13:15, and 18:45 minus 5 hours 30 minutes is 13:15. the Z at the end just means an offset of zero.

i kept reading +05:30 as a typo. offsets dont have to be whole hours, and India sits at exactly 5 hours 30 minutes ahead, so code that stores the offset as a whole number of hours quietly breaks for Mumbai.

one caveat, an offset is not a time zone. -04:00 is what New York uses in April, but in winter it uses -05:00, so the offset alone cant tell you what the clock will say in January. thats the next problem.

so what: the written internet standard for timestamps, RFC 3339, defines exactly this +hh:mm ending (https://www.rfc-editor.org/rfc/rfc3339). a timestamp string without one is a guess you make later, usually wrong.

### check yourself

1. order 102 shows 18:40 on a Mumbai clock, which is 5 hours 30 minutes ahead of UTC. predict its UTC time.
```sql
SELECT ordered_at - INTERVAL '5 hours 30 minutes' AS utc FROM orders WHERE order_id = 102;
```
<details><summary>answer</summary>

```result
utc
2026-04-01 13:10:00
```
undo the offset by subtracting it. the tempting answer is adding it, 00:10 the next day, which pushes the clock further from UTC instead of back to it.

</details>

2. one log line says 10:00 with offset +02:00, another says 07:30 with offset -01:00, same day. which happened first?
<details><summary>answer</summary>

the 10:00 line. undone, it is 08:00 UTC, and the 07:30 line is 08:30 UTC. the tempting answer is the 07:30 line, from comparing the clock text without the offsets.

</details>

---
prev: [027 dates without times, and times without dates](./027-dates-and-times-apart.md) | next: not written yet
