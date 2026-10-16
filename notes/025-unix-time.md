# 025: unix time, counting seconds from 1970
builds on: [001 data is facts written down](./001-data-is-facts-and-numbers.md), [002 bits](./002-bits.md), [003 counting in binary](./003-counting-in-binary.md), [016 overflow](./016-overflow.md), [024 UTC, the worlds reference clock](./024-utc.md)
section: data at the atom level, part 25, ~2 min read

[024](./024-utc.md) read one moment three ways: 13:15 in UTC, the clock with no daylight saving, 09:15 in New York, 18:45 in Mumbai. what if the database kept none of those readings and you just stored one plain number?

unix time is a moment kept as a count of seconds since 00:00:00 UTC on 1 January 1970, a starting line called the epoch. the shops order 101, from the imaginary gujarati snack store these notes run on, is the same moment on every clock. i take its 09:15 as New York time like 024 did, while [001](./001-data-is-facts-and-numbers.md) read it as UTC, 14400 seconds earlier.

```python
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

moment = datetime(2026, 4, 1, 13, 15, tzinfo=timezone.utc)
print(int(moment.timestamp()))
print(int(moment.astimezone(ZoneInfo("America/New_York")).timestamp()))
print(int(moment.astimezone(ZoneInfo("Asia/Kolkata")).timestamp()))
later = moment + timedelta(hours=1)
print(int(later.timestamp()) - int(moment.timestamp()))
```

```output
1775049300
1775049300
1775049300
3600
```

i assumed a stored moment carried its time zone around with it, but a single number has nowhere to put one, a zone is only needed to show it as clock text. New York, Mumbai and UTC all give 1775049300. sorting is just sorting numbers, and an hour later is exactly 3600 more.

before 1970 the count goes negative, so -1 is 23:59:59 UTC on 31 December 1969. one caveat: unix time ignores leap seconds, an extra second the world clock sometimes adds, so every day is exactly 86400 seconds, 24 times 60 times 60.

so what: [003](./003-counting-in-binary.md) mentioned the 2038 bug. a counter with 32 switches ([bits](./002-bits.md)) tops out at 2147483647 when signed, which is 03:14:07 UTC on 19 January 2038, and one more second [overflows](./016-overflow.md), wrapping to 1901. https://en.wikipedia.org/wiki/Unix_time

why do so many systems count in thousandths of a second? next one.

---
prev: [024 UTC, the worlds reference clock](./024-utc.md) | next: [026 seconds, milliseconds, microseconds](./026-seconds-milliseconds-microseconds.md)
