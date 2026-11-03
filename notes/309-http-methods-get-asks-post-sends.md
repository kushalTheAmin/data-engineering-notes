# 309: HTTP methods, GET asks and POST sends
builds on: [307 URLs and query parameters](./307-urls-and-query-parameters.md), [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md)
section: talking over a network, part 4, ~2 min read

what happens if Bhavins phone sends the same message twice? for one kind of request, nothing. for another kind, he gets two orders.

an HTTP method is the first word of a request, the one [308](./308-request-and-response-one-message-out-one-message-back.md) left unexplained in `GET /orders ...`. it isnt a python method, its just a word telling the server what kind of thing you want done. GET means "give me this", POST means "here is data, act on it". below is a toy shop server (the shop, the imaginary gujarati snack store these notes run on) with the 7 order ids, and Bhavins phone (the client, the side that asks) sending requests like the ones in 308, where Content-Length says the body is 13 characters:

```python
orders = [101, 102, 103, 104, 105, 106, 107]

def shop(request):
    head, body = request.split("\r\n\r\n")
    method = head.split(" ")[0]
    if method == "GET":
        return f"{len(orders)} orders"
    if method == "POST":
        orders.append(orders[-1] + 1)
        return f"new order {orders[-1]}"

get = "GET /orders HTTP/1.1\r\nHost: shop.example\r\n\r\n"
post = "POST /orders HTTP/1.1\r\nHost: shop.example\r\nContent-Length: 13\r\n\r\ncustomer_id=2"
for r in (get, get, post, post, get):
    print(r.split(" ")[0].ljust(4), shop(r))
```

```output
GET  7 orders
GET  7 orders
POST new order 108
POST new order 109
GET  9 orders
```

GET only reads, so sending it twice changes nothing. POST carries data in its body (the part after the empty line, here customer_id=2) and the server adds something, so twice means two orders.

i assumed an identical message would give an identical result, but the first word decides, and POST doesnt promise it. the toy server cant tell the second POST is a repeat.

this bites in real apps. the HTTP spec (RFC 9110) says a client shouldnt automatically retry a method like POST, since the first try may already have worked. PUT (replace a thing) and DELETE (remove it) are safe to repeat, so POST is the odd one.

### check yourself

1. Asha already has orders 101, 103 and 106. her phone sends POST /orders for customer_id=1, the connection drops before any answer, and the app resends it. the first one did arrive. how many orders does she have now?
<details><summary>answer</summary>

she had 3, and each POST that arrived added one, so 5. the tempting answer is 4, from thinking she tapped once, but the server saw two messages and cant know the second was a retry.

</details>

2. a script sends DELETE for order 104 twice. does the second one remove another order?
<details><summary>answer</summary>

no. the first removes 104, and after that the second has nothing left to remove, so the shop ends up the same as after one. the tempting wrong answer is yes, as if DELETE meant "remove one more". the answer may be an error message, but the data doesnt change again.

</details>

---
prev: [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md) | next: not written yet
