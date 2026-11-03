# 308: request and response, one message out, one message back
builds on: [042 line endings, the invisible characters that break files](./042-line-endings.md), [086 client and server, you ask, the database answers](./086-client-and-server.md), [307 URLs and query parameters](./307-urls-and-query-parameters.md)
section: talking over a network, part 3, ~2 min read

what does Ashas phone send when she taps "my delivered orders"? i pictured something fancy, and in plain HTTP/1.1 its a few lines of text (real phones encrypt it, and newer versions pack it as binary).

HTTP, the rules the web talks by (the http at the start of a [URL](./307-urls-and-query-parameters.md)), has two kinds of message. a request is the text a [client](./086-client-and-server.md) (the side that asks) sends, and a response is the text the server sends back. here it is for the shop, the imaginary gujarati snack store these notes run on, both ends on this machine like in [086](./086-client-and-server.md), with each [line ending](./042-line-endings.md) (characters that end a line) shown as \r\n:

```python
import socket

server = socket.socket()
server.bind(("127.0.0.1", 0))
server.listen()
port = server.getsockname()[1]

client = socket.create_connection(("127.0.0.1", port))
client.sendall(b"GET /orders?customer_id=1&status=delivered HTTP/1.1\r\nHost: shop.example\r\n\r\n")
conn, _ = server.accept()
print("request :", repr(conn.recv(1000).decode()))
conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 10\r\n\r\n[101, 103]")
print("response:", repr(client.recv(1000).decode()))
```

```output
request : 'GET /orders?customer_id=1&status=delivered HTTP/1.1\r\nHost: shop.example\r\n\r\n'
response: 'HTTP/1.1 200 OK\r\nContent-Length: 10\r\n\r\n[101, 103]'
```

both messages have the same shape: a first line, some extra lines, an empty line, then an optional body. the request first line says what you want, the path and query from the [URL](./307-urls-and-query-parameters.md). the response first line says how it went, and the body is the answer, here Ashas delivered orders, 101 and 103. GET, the Host line and 200 each get their own note later. the extra lines are called headers.

i expected a special format a human could never type, but you could write it by hand. the empty line is how the reader knows the top part is over, and the Content-Length header says the body is 10 bytes (one per character here). a client that obeys the number without checking would keep only 5 bytes of it, `[101,`, if it said 5.

### check yourself

1. you hand-write a request as `GET /orders HTTP/1.1\r\nHost: shop.example\r\n`, one \r\n at the end instead of two. a typical server answers instantly, waits, or errors at once?
<details><summary>answer</summary>

it typically waits, then gives up with a timeout error. without the empty line the server cant tell the top part is finished, so it waits for more lines while you wait for the answer. "instantly" is the tempting guess, because everything you wanted is already in the message.

</details>

2. Bhavin asks for Ashas pending orders, `customer_id=1&status=pending`. what Content-Length should the shop send for a body written like `[101, 103]`, in a list with brackets? (the SQL just finds the order ids.)

```sql
SELECT order_id FROM orders WHERE customer_id = 1 AND status = 'pending' ORDER BY order_id
```
<details><summary>answer</summary>

```result
order_id
106
```

the answer is 5. the query returns one row, so the body is `[106]`, 5 bytes, all ASCII. the tempting answers are 1, from counting rows, or 3, from counting only the digits, but the header counts every byte of the body, brackets too.

</details>

---
prev: [307 URLs and query parameters](./307-urls-and-query-parameters.md) | next: [309 HTTP methods, GET asks and POST sends](./309-http-methods-get-asks-post-sends.md)
