# 310: HTTP headers, notes attached to a request
builds on: [065 the header row, naming the columns](./065-the-header-row-naming-the-columns.md), [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [306 DNS, turning names into addresses](./306-dns-turning-names-into-addresses.md), [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md)
section: talking over a network, part 5, ~2 min read

after [DNS](./306-dns-turning-names-into-addresses.md) (the lookup from name to address) the phone connects to the address 192.0.2.10, and the name isnt part of that. so how does the machine know which site you wanted?

a header is one `Name: value` line in an HTTP message (the [request or response](./308-request-and-response-one-message-out-one-message-back.md) text), between the first line and the empty line. the Host header carries the name. [065](./065-the-header-row-naming-the-columns.md) had a header row too, a different thing, the column names of a csv. here is Ashas phone asking the shop, the imaginary gujarati snack store these notes run on:

```text
GET /orders?customer_id=1&status=delivered HTTP/1.1     first line: method and path
Host: shop.example                     which site, the name the address lacks
Accept: application/json               the format i prefer

HTTP/1.1 200 OK                        first line: how it went
Content-Type: application/json         the body is JSON
Content-Length: 10                     body size, 1 byte a character

[101, 103]                             the body
```

[JSON](./066-json-records-with-names-on-every-value.md) is text with names on every value. each header is a key and a value, so i read the top part as a dictionary written as text. turning it back into one is a small loop (the happy path, a repeated header would overwrite):

```python
# \r\n ends a line, \r\n\r\n is the empty line
raw = "GET /orders HTTP/1.1\r\nHost: shop.example\r\nAccept: application/json\r\n\r\n"
headers = {}
for line in raw.split("\r\n\r\n")[0].split("\r\n")[1:]:
    name, value = line.split(": ", 1)
    headers[name.lower()] = value
print(headers)
print(headers["host"])
```

```output
{'host': 'shop.example', 'accept': 'application/json'}
shop.example
```

i lowercased the names because HTTP ignores case in them, so Host and host are the same header. skip that and your lookup misses a header thats plainly there.

most request headers say what the client wants, most response headers describe the body. a body is just bytes, so Content-Type is the main thing saying how to read them.

this is how one machine at one address serves many sites: HTTP/1.1 requires a client to send Host, and the server (the program answering) picks the site by it. i figured the extra lines were decoration, but the name the address doesnt carry has to ride along in one of them.

---
prev: [309 HTTP methods, GET asks and POST sends](./309-http-methods-get-asks-post-sends.md) | next: not written yet
