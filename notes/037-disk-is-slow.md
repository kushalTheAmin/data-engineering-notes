# 037: disk is slow, memory vs SSD vs spinning disk in real numbers
builds on: [026 seconds, milliseconds, microseconds](./026-seconds-milliseconds-microseconds.md), [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md)
section: memory, disks and files, part 3, ~2 min read

[036](./036-memory-vs-disk.md) said disk keeps your bytes and memory forgets them. so how much slower is disk, really? the numbers look tiny until you stretch them.

a lookup here means fetching one value from a random spot. from an old, widely shared table of latency numbers: memory takes 100 nanoseconds (a billionth of a second), an SSD (a disk made of chips) 150 microseconds, and a spinning hard drive about 10 milliseconds, mostly moving a read head into place. micro and milli were built in [026](./026-seconds-milliseconds-microseconds.md), a millionth and a thousandth of a second.

now say 1 nanosecond lasts 1 second. the shop, the imaginary gujarati snack store these notes run on, wants order 101 from a random spot:

```python
lookups = {"memory": 100, "SSD": 150_000, "spinning disk": 10_000_000}
for name, ns in lookups.items():
    d, rest = divmod(ns, 86400)
    h, rest = divmod(rest, 3600)
    m, s = divmod(rest, 60)
    print(f"{name:>13}: {ns:>10,} ns = {d} days {h} h {m} min {s} s")
```

```output
       memory:        100 ns = 0 days 0 h 1 min 40 s
          SSD:    150,000 ns = 1 days 17 h 40 min 0 s
spinning disk: 10,000,000 ns = 115 days 17 h 46 min 40 s
```

memory hands it over in under two minutes, the SSD makes you wait almost two days, the spinning disk nearly four months. i assumed an SSD was close to memory, but its 1500 times slower per lookup. still 67 times faster than the spinning disk.

caveat: the table is old and drives have improved, so read it as the size of the gap. and it prices a jump to a random spot; a later note covers reading along a file.

this is why databases keep a chunk of memory for recently used data, PostgreSQL, a popular server database, has a setting for it called shared_buffers.

### check yourself

1. a program looks up 1000 orders, each at a random spot on a spinning disk, at 10 milliseconds each. how long does it wait in total?
<details><summary>answer</summary>

```python
print(1000 * 10_000_000 / 1_000_000_000, "seconds")
```

```output
10.0 seconds
```
10 seconds. the tempting answer is 10 milliseconds, from forgetting that every lookup pays the wait again.

</details>

2. someone says moving the shop from a spinning disk to an SSD makes lookups 1500 times faster. what is the real ratio for one lookup?
<details><summary>answer</summary>

```python
print(round(10_000_000 / 150_000, 1))
```

```output
66.7
```
about 67 times. 1500 is SSD against memory, a different pair. and a query also spends time on the processor, so the whole query wont speed up by that much either.

</details>

---
prev: [036 memory vs disk, one forgets and one remembers](./036-memory-vs-disk.md) | next: not written yet
