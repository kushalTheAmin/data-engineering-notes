# 029: daylight saving, the hour that happens twice
builds on: [024 UTC, the worlds reference clock](./024-utc.md), [025 unix time, counting seconds from 1970](./025-unix-time.md), [028 time zones, offsets from UTC](./028-time-zone-offsets.md)
section: data at the atom level, part 29, ~2 min read

can two different moments show the exact same clock reading in one city? on 1 November 2026 in New York they do. 01:30 happens twice that night.

daylight saving is when a place moves its clocks by an hour twice a year. [UTC](./024-utc.md), the one reference clock, never moves. in the fall New York sets its clock back an hour, so the hour after 01:00 is lived twice, first with an [offset](./028-time-zone-offsets.md) of -04:00 (hours behind UTC), then -05:00. here is that night with the [unix time](./025-unix-time.md), (seconds counted since 1970) of each moment:

| UTC | New York clock | offset | unix time |
|---|---|---|---|
| 04:30 | 00:30 | -04:00 | 1793507400 |
| 05:30 | 01:30 | -04:00 | 1793511000 |
| 06:30 | 01:30 | -05:00 | 1793514600 |
| 07:30 | 02:30 | -05:00 | 1793518200 |

look at the middle two rows. same clock text, 01:30, but the unix times differ by 3600 seconds, one full hour. say Asha, a shop customer in Jersey City (same clock as New York), ordered at 01:30 that night. this is a made up order, not a shop row. the text 2026-11-01 01:30:00 is an ambiguous time, a reading that fits two moments, and it cant tell you which one.

i figured a clock reading was at least unique inside one city, and it is, except for this one hour a year. the offset is the only thing that separates the two.

in spring its the reverse: clocks jump from 02:00 to 03:00, so 02:30 on 8 March 2026 never appears on a New York clock at all.

so what: Pythons datetime has a fold flag (PEP 495) that exists purely to say "first or second 01:30". local time stored without an offset has to guess, wrong for one hour every fall.

### check yourself

1. two New York log lines from 1 November 2026: "01:50 with offset -04:00" and "01:10 with offset -05:00". sorted by clock text the 01:10 line comes first. which really happened first?
<details><summary>answer</summary>

the 01:50 line. undone it is 05:50 UTC, and the 01:10 line is 06:10 UTC. the tempting answer is 01:10, from reading the clock text and ignoring the offsets.

</details>

2. the shop clocks are New York time. a report adds 5 hours to every ordered_at to get UTC, because "New York is -05:00". predict its result for order 106, and say what UTC really is.
```sql
SELECT ordered_at + INTERVAL '5 hours' AS utc FROM orders WHERE order_id = 106;
```
<details><summary>answer</summary>

```result
utc
2026-04-08 15:00:00
```
on 8 April New York is on -04:00, so the real UTC is 14:00 and the report is an hour off. the tempting answer is that 15:00 is right, because -05:00 is the winter offset and feels like New Yorks number.

</details>

---
prev: [028 time zones, offsets from UTC](./028-time-zone-offsets.md) | next: not written yet
