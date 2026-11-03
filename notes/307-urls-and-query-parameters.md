# 307: URLs and query parameters
builds on: [053 absolute vs relative paths](./053-absolute-vs-relative-paths.md), [306 DNS, turning names into addresses](./306-dns-turning-names-into-addresses.md), [085 addresses and ports, the right program on the right machine](./085-addresses-and-ports.md), [086 client and server, you ask, the database answers](./086-client-and-server.md), [278 hash tables, how a dictionary finds a key without searching](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md)
section: talking over a network, part 2, ~2 min read

how does a web address say "Ashas delivered orders" and not just "the shop"? [306](./306-dns-turning-names-into-addresses.md) turned a name into an address, but people type a name inside a longer string, and the name is only one piece of it.

a URL is one text string that holds everything needed to ask for something, split into parts by fixed punctuation. here is one for the shop, the imaginary gujarati snack store these notes run on:

```text
http://shop.example:8080/orders?customer_id=1&status=delivered
|      |            |    |      |
|      |            |    |      query: filters, key=value joined by &
|      |            |    path: which thing on that server
|      |            port: which program (085)
|      host name: looked up by DNS (306)
scheme: the rules for talking
```

the host name goes to DNS, the [port](./085-addresses-and-ports.md) (a number picking one program) picks the program, and the [server](./086-client-and-server.md) (the side that waits for requests) reads the path and the query. this path is not the file path of [053](./053-absolute-vs-relative-paths.md), it just names a thing on the server. the query starts at the ? and usually holds key=value pairs, so it is often a [dictionary](./278-hash-tables-how-a-dictionary-finds-a-key-without-searching.md) written as text. python can split it:

```python
from urllib.parse import urlsplit, parse_qs
url = "http://shop.example:8080/orders?customer_id=1&status=delivered"
p = urlsplit(url)
print(p.scheme, p.hostname, p.port, p.path, sep=" | ")
print(parse_qs(p.query))
```

```output
http | shop.example | 8080 | /orders
{'customer_id': ['1'], 'status': ['delivered']}
```

i expected `1` to come back as a number, but everything in a URL is text, so the server has to turn '1' into 1 itself. each value is also a list, because a key may appear twice, like status=pending&status=delivered.

so to ask for a filtered list, you add a query parameter, a filter written into the address. the shop would answer this one with Ashas delivered orders, 101 and 103.

---
prev: [306 DNS, turning names into addresses](./306-dns-turning-names-into-addresses.md) | next: [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md)
