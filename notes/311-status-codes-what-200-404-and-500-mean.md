# 311: status codes, what 200, 404 and 500 mean
builds on: [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md), [309 HTTP methods, GET asks and POST sends](./309-http-methods-get-asks-post-sends.md), [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md)
section: talking over a network, part 6, ~2 min read

every response in [308](./308-request-and-response-one-message-out-one-message-back.md) and [310](./310-http-headers-notes-attached-to-a-request.md) started with `HTTP/1.1 200 OK`. so what does the shop send when you ask for an order that doesnt exist, or when its own code blows up?

a status code is the 3 digit number on the first line of a response, saying how the request went. the first digit is the class, and the class tells you whose problem it is:

| first digit | means | who has to change something |
|---|---|---|
| 2xx | it worked | nobody |
| 4xx | the request was wrong | the client |
| 5xx | the server failed | the server |

(1xx and 3xx exist too, 3xx is mostly redirects, sending you somewhere else.) here is a toy server for the shop, the imaginary gujarati snack store these notes run on, holding a slice of its orders:

```python
orders = {101: "delivered", 104: "cancelled"}

def shop(path, database_up=True):
    if not database_up:
        return 500
    order_id = int(path.split("/")[-1])
    return 200 if order_id in orders else 404

print("GET /orders/101", shop("/orders/101"))
print("GET /orders/104", shop("/orders/104"))
print("GET /orders/999", shop("/orders/999"))
print("GET /orders/101", shop("/orders/101", database_up=False))
```

```output
GET /orders/101 200
GET /orders/104 200
GET /orders/999 404
GET /orders/101 500
```

404 means the server found nothing there, or wont say if anything is. 500 means the server hit something unexpected, and the same request that gave 200 gives 500 once the database is down.

i assumed a cancelled order would come back as an error, but 104 is a 200. the code is about the request, and the bad news lives in the body (the part after the empty line).

this bites in real code: the browser fetch call in javascript doesnt throw on a 404 or 500, you have to check response.ok yourself (MDN says so). as a rule of thumb, retrying a 4xx unchanged usually gets the same answer, and a 5xx may pass next time.

### check yourself

1. Bhavins phone asks a shop that holds all 7 real orders (the toy above holds only two) for order 107 and then for order 108. which codes come back?
```sql
SELECT order_id FROM orders WHERE order_id IN (107, 108)
```
<details><summary>answer</summary>

```result
order_id
107
```

200, then 404. only 107 exists, and the server is fine, so a missing order is the clients mistake. the tempting wrong answer is 500 for 108, but nothing broke, the server just found nothing.

</details>

2. the app sends POST /orders and gets 500 back. it resends the same POST right away, since "the server failed, so nothing was saved". what did this assume, and why is it risky?
<details><summary>answer</summary>

it assumed the failure came before the order was saved. a server can fail after saving (say while writing the response), so the resend might add a second order, like in [309](./309-http-methods-get-asks-post-sends.md). a 500 only says something unexpected broke, not how far it got.

</details>

---
prev: [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md) | next: [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md)
