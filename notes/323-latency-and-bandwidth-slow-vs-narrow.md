# 323: latency and bandwidth, slow vs narrow
builds on: [026 seconds, milliseconds, microseconds](./026-seconds-milliseconds-microseconds.md), [033 kilobytes to terabytes](./033-kilobytes-to-terabytes.md), [037 disk is slow, memory vs SSD vs spinning disk in real numbers](./037-disk-is-slow.md), [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md), [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md), [322 encryption in transit, TLS and https](./322-encryption-in-transit-tls-and-https.md)
section: talking over a network, part 18, ~2 min read

[322](./322-encryption-in-transit-tls-and-https.md) made the connection safe, not fast. so why does a script fetching 100 orders one request at a time take about 72 times longer than asking once (toy numbers below), when the same data moves?

"slow" hides two different costs. latency is the wait, out and back, for a [request](./308-request-and-response-one-message-out-one-message-back.md) and its answer, even if it carries nothing (counted in [milliseconds](./026-seconds-milliseconds-microseconds.md), same idea as the waits in [037](./037-disk-is-slow.md)). bandwidth is how many bytes the connection moves per second. think of a road: latency is how long it is, bandwidth is how many lanes.

toy numbers for the shop, the imaginary gujarati snack store these notes run on: 50 ms out and back, one order record is a made-up 200 bytes, and bandwidth is 1 or 10 [MB](./033-kilobytes-to-terabytes.md) (a million bytes) per second.

```python
latency = 0.05        # seconds, out and back
order = 200           # bytes in one order record

def seconds(requests, size_each, bandwidth):
    return requests * (latency + size_each / bandwidth)

jobs = {
    "100 requests, 1 order each": (100, order),
    "1 request, all 100 orders": (1, 100 * order),
    "1 request, a 100 MB export": (1, 100_000_000),
}
print(f"{'seconds':28}{'1 MB/s':>9}{'10 MB/s':>9}")
for name, (n, size) in jobs.items():
    slow = seconds(n, size, 1_000_000)
    fast = seconds(n, size, 10_000_000)
    print(f"{name:28}{slow:9.3f}{fast:9.3f}")
```

```output
seconds                        1 MB/s  10 MB/s
100 requests, 1 order each      5.020    5.002
1 request, all 100 orders       0.070    0.052
1 request, a 100 MB export    100.050   10.050
```

every request pays the 50 ms, so the first row waits 5 seconds to move 0.02 seconds of data. a connection 10 times wider saves 0.018 seconds there. width matters most in the last row, where the wait is nothing next to the bytes. i assumed a faster connection fixed everything, but for small requests it barely moves anything.

this is why [APIs](./312-apis-a-door-built-for-programs.md) let you ask for many rows per request. GitHubs API takes a per_page setting, max 100 on most requests, and if you ask for more it quietly lowers it instead of erroring ([GitHub docs](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)). the toy skips the address lookup and the [https handshake](./322-encryption-in-transit-tls-and-https.md), which add waits too.

### check yourself

1. Ashas 3 orders (101, 103, 106) are fetched with one request each, 50 ms out and back, tiny answers. how long is the waiting, and what is it if one request returns all 3?
<details><summary>answer</summary>

3 x 0.05 = 0.15 seconds against 0.05 for one request. the tempting answer is that the same bytes take the same time, but each request pays the wait again.

</details>

2. the team upgrades from 1 MB/s to 100 MB/s. which job gets about 100 times faster, 100 requests of 200 bytes or one 100 MB export?
<details><summary>answer</summary>

the export: 100.05 seconds drops to 1.05. the 100 small requests go from 5.02 to 5.0002, because 5 seconds of that is latency. the tempting answer is both, from thinking a faster line speeds up everything.

</details>

3. 10000 order records (200 bytes each, so 2 million bytes) at 1 MB/s. pages of 100 rows means 100 requests, pages of 1000 means 10. is the second 10 times faster?
<details><summary>answer</summary>

no. the data always needs 2 seconds. 100 requests wait 5 + 2 = 7 seconds, 10 requests wait 0.5 + 2 = 2.5 seconds, so about 2.8 times faster. fewer requests only removes the latency part.

</details>

---
prev: [322 encryption in transit, TLS and https](./322-encryption-in-transit-tls-and-https.md) | next: not written yet
