# 313: JSON over HTTP, the answer is text until you parse it
builds on: [066 JSON, records with names on every value](./066-json-records-with-names-on-every-value.md), [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md), [308 request and response, one message out, one message back](./308-request-and-response-one-message-out-one-message-back.md), [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md), [311 status codes, what 200, 404 and 500 mean](./311-status-codes-what-200-404-and-500-mean.md), [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md)
section: talking over a network, part 8, ~2 min read

in [312](./312-apis-a-door-built-for-programs.md) the report script got "the ids" back from the shop API. so what is actually in its hands when the answer arrives, a python list?

a JSON answer is a [response](./308-request-and-response-one-message-out-one-message-back.md) (the text a server sends back) whose body is [JSON](./066-json-records-with-names-on-every-value.md) text, and a Content-Type [header](./310-http-headers-notes-attached-to-a-request.md) (a Name: value line before the body) says so. here is the shop, the imaginary gujarati snack store these notes run on, answering GET /orders?customer_id=1, a slice of 2 fields per order:

```text
HTTP/1.1 200 OK
Content-Type: application/json

[{"order_id": 101, "status": "delivered"}, {"order_id": 103, "status": "delivered"}, {"order_id": 106, "status": "pending"}]
```

```python
import json
body = '[{"order_id": 101, "status": "delivered"}, {"order_id": 103, "status": "delivered"}, {"order_id": 106, "status": "pending"}]'
print(type(body).__name__, body[0])
orders = json.loads(body)
print(type(orders).__name__, orders[2]["status"])
print([o["order_id"] for o in orders if o["status"] == "delivered"])
try:
    json.loads("<html>oops</html>")
except json.JSONDecodeError:
    print("not json")
```

```output
str [
list pending
[101, 103]
not json
```

i figured the script got a list, but all that crosses the wire is characters. body[0] is just the character [, and the list only appears once json.loads runs. after that its a list of dictionaries, one per order, like the rows in [066](./066-json-records-with-names-on-every-value.md), and the script asks for fields by name.

that is why the shop can add a total field tomorrow without breaking this loop, since the script only asks for the names it uses.

the gotcha: Content-Type is only a label, nothing forces the body to match it. a [500](./311-status-codes-what-200-404-and-500-mean.md) can come with an error page that isnt JSON, and json.loads on it raises an error, like the last line shows. check the status code before you parse.

---
prev: [312 APIs, a door built for programs](./312-apis-a-door-built-for-programs.md) | next: [314 API keys, a password for programs](./314-api-keys-a-password-for-programs.md)
