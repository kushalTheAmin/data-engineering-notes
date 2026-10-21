# 030: store in UTC, show in local time
builds on: [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md), [028 time zones, offsets from UTC](./028-time-zone-offsets.md), [029 daylight saving, the hour that happens twice](./029-daylight-saving.md)
section: data at the atom level, part 30, ~2 min read

[029](./029-daylight-saving.md) left two different moments wearing the same 01:30. so what should a timestamp column actually hold, so that never happens?

the habit: store every moment in [UTC](./024-utc.md), the one reference clock that never shifts, and convert to a local clock only at the last second, when a human is about to look at it.

the shop, the imaginary gujarati snack store these notes run on, keeps ordered_at as New York clock text. below i undo Aprils offset of -04:00 (subtract it, so 09:15 becomes 13:15) to get the UTC column, then show each order on two screens, using Mumbais +05:30 from [028](./028-time-zone-offsets.md). a slice of 3 orders:

| order | stored (UTC) | New York screen | Mumbai screen |
|---|---|---|---|
| 101 | 2026-04-01 13:15 | 2026-04-01 09:15 | 2026-04-01 18:45 |
| 102 | 2026-04-01 22:40 | 2026-04-01 18:40 | 2026-04-02 04:10 |
| 106 | 2026-04-08 14:00 | 2026-04-08 10:00 | 2026-04-08 19:30 |

the stored column never changes, the screens just read it differently. order 102 even lands on a different date in Mumbai. sorting, comparing and subtracting only ever touch the first column, so there is no offset to forget.

and the 01:30 problem from 029 disappears, because the two moments are stored as two different values. the python below does the conversion at the screen:

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")
for h in [5, 6]:
    utc = datetime(2026, 11, 1, h, 30, tzinfo=timezone.utc)
    print(utc.isoformat(), "->", utc.astimezone(ny).isoformat())
```

```output
2026-11-01T05:30:00+00:00 -> 2026-11-01T01:30:00-04:00
2026-11-01T06:30:00+00:00 -> 2026-11-01T01:30:00-05:00
```

i figured storing the time exactly as the customer saw it was the faithful choice. its the lossy one, because the offset is the part you cant recover.

so what: Postgres, a server database, works this way. its timestamp with time zone type stores UTC internally and converts to the sessions time zone on output, and the original zone is not kept (https://www.postgresql.org/docs/current/datatype-datetime.html). if you need the customers zone later, store it in its own column.

### check yourself

1. a dashboard converts the shops New York clock to Mumbais, 9 hours 30 minutes ahead in April. predict the day it shows for orders 101 and 102. SELECT picks columns, FROM names the table, WHERE keeps matching rows, INTERVAL is a length of time, ::DATE keeps only the day.
```sql
SELECT order_id, (ordered_at + INTERVAL '9 hours 30 minutes')::DATE AS mumbai_day FROM orders WHERE order_id IN (101, 102);
```
<details><summary>answer</summary>

```result
order_id | mumbai_day
101 | 2026-04-01
102 | 2026-04-02
```
order 102 is 18:40 in New York, and adding 9:30 passes midnight, so Mumbai calls it 2 April. the tempting answer is 1 April for both, from assuming one order has one date everywhere.

</details>

2. a car park stores New York clock text only. a car entered at 2026-11-01 00:30 and left at 2026-11-01 02:30, and the job subtracts the texts to bill 2 hours. how long was it really there?
<details><summary>answer</summary>

3 hours. 00:30 is -04:00, so 04:30 UTC, and 02:30 is -05:00 after the clocks went back, so 07:30 UTC. the tempting answer is 2 hours, from subtracting clock text across the extra hour.

</details>

---
prev: [029 daylight saving, the hour that happens twice](./029-daylight-saving.md) | next: [031 null, a marker for a missing value](./031-null.md)
