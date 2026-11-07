# 351: connection pools, why opening a connection is expensive
builds on: [350 connecting python to a database, a result you read once](./350-connecting-python-to-a-database-a-result-you-read-once.md), [323 latency and bandwidth, slow vs narrow](./323-latency-and-bandwidth-slow-vs-narrow.md), [322 encryption in transit, TLS and https](./322-encryption-in-transit-tls-and-https.md), [212 connections and sessions, one conversation with the database](./212-connections-and-sessions-one-conversation-with-the-database.md), [211 a database server, Postgres where most app data lives](./211-a-database-server-postgres-where-most-app-data-lives.md)
section: python for data work, part 27, ~2 min read

a script of mine ran one tiny query per page load and it still felt slow. the query was never the problem, so where did the time go?

a connection pool is a handful of [connections](./102-a-database-in-one-file.md) (open lines to the database) that get opened once and kept open. your code borrows one for a query and hands it back, instead of opening a fresh one each time. [350](./350-connecting-python-to-a-database-a-result-you-read-once.md) did connect, execute, fetch, and connect looked free.

it isnt free. a new line needs several waits before your first query: reach the server, the [TLS handshake](./322-encryption-in-transit-tls-and-https.md) (agreeing a secret key) if locked, then logging in. each wait is a [round trip](./323-latency-and-bandwidth-slow-vs-narrow.md). Postgres also starts a new server process per connection. here are toy numbers for the shop, the imaginary gujarati snack store these notes run on: opening takes 150 ms (3 waits), a query takes 50 ms (1 wait),.

```python
OPEN, QUERY = 150, 50   # ms, toy numbers: opening is 3 waits, a query is 1

def no_pool(n):
    return n * (OPEN + QUERY)

def pooled(n):
    ready, spent = [], 0
    for _ in range(n):
        if ready:
            conn = ready.pop()
        else:
            conn = "open line"
            spent += OPEN
        spent += QUERY
        ready.append(conn)
    return spent

print("100 page loads, one query each")
print("new connection every time:", no_pool(100), "ms")
print("borrow from a pool       :", pooled(100), "ms")
```

```output
100 page loads, one query each
new connection every time: 20000 ms
borrow from a pool       : 5150 ms
```

the pool pays the 150 once, on the first load. every load after that borrows the open line from ready and puts it back. i assumed the query was the cost, but 15000 of those 20000 ms were just getting a line open.

so what: Postgres allows 100 connections by default (max_connections, [Postgres docs](https://www.postgresql.org/docs/current/runtime-config-connection.html)), so 100 app copies each opening their own fills it, and a pool caps how many lines you hold. a borrowed connection nobody hands back is gone, and the pool runs dry. PgBouncer from [212](./212-connections-and-sessions-one-conversation-with-the-database.md) is a pool that sits in front of [Postgres](./211-a-database-server-postgres-where-most-app-data-lives.md).

---
prev: [350 connecting python to a database, a result you read once](./350-connecting-python-to-a-database-a-result-you-read-once.md) | next: not written yet
