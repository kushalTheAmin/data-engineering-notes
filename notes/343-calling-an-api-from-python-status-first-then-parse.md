# 343: calling an API from python, status first, then parse
builds on: [342 environment variables, settings that live outside the code](./342-environment-variables-settings-that-live-outside-the-code.md), [341 reading JSON in python, the whole file at once](./341-reading-json-in-python-the-whole-file-at-once.md), [335 with, opening and closing things safely](./335-with-opening-and-closing-things-safely.md), [334 errors in scripts, catching them without hiding them](./334-errors-in-scripts-catching-them-without-hiding-them.md), [314 API keys, a password for programs](./314-api-keys-a-password-for-programs.md), [313 JSON over HTTP, the answer is text until you parse it](./313-json-over-http-the-answer-is-text-until-you-parse-it.md), [311 status codes, what 200, 404 and 500 mean](./311-status-codes-what-200-404-and-500-mean.md), [310 HTTP headers, notes attached to a request](./310-http-headers-notes-attached-to-a-request.md)
section: python for data work, part 19, ~2 min read

i expected a 404 from an [API](./312-apis-a-door-built-for-programs.md), a door for programs, to come back like any other answer, something i could check. python raised an error instead.

calling an API from python means building a request, a URL plus a [header](./310-http-headers-notes-attached-to-a-request.md) (a Name: value line), and getting back a [status code](./311-status-codes-what-200-404-and-500-mean.md) and a body that is [JSON text](./313-json-over-http-the-answer-is-text-until-you-parse-it.md) until you parse it, meaning turn it into python values. the [API key](./314-api-keys-a-password-for-programs.md), a secret string, rides in that header. it comes from an [environment variable](./342-environment-variables-settings-that-live-outside-the-code.md), named text the operating system hands your script. the top half below is a pretend API for the shop, the imaginary gujarati snack store these notes run on, so skip it. get returns a pair, the status and the body:

```python
import json, os, threading, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

class Shop(BaseHTTPRequestHandler):  # a pretend shop API, running on this machine
    def do_GET(self):
        orders = {"/orders/101": {"order_id": 101, "customer_id": 1, "status": "delivered"}}
        if self.headers.get("x-api-key") != "k_report_7f3a":
            code, body = 401, "unknown caller"
        elif self.path in orders:
            code, body = 200, json.dumps(orders[self.path])
        else:
            code, body = 404, "no such order"
        self.send_response(code)
        self.end_headers()
        self.wfile.write(body.encode())
    def log_message(self, *args):
        pass

server = HTTPServer(("127.0.0.1", 0), Shop)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = "http://127.0.0.1:%d" % server.server_port

os.environ["SHOP_API_KEY"] = "k_report_7f3a"  # normally set in the terminal

def get(path, key):
    req = urllib.request.Request(base + path, headers={"x-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode()

key = os.environ["SHOP_API_KEY"]
print(get("/orders/101", key))
print(get("/orders/101", "k_report_7f3"))
print(get("/orders/999", key))
```

```output
(200, {'order_id': 101, 'customer_id': 1, 'status': 'delivered'})
(401, 'unknown caller')
(404, 'no such order')
```

only the 200 body is JSON (200 fine, 401 unknown caller, 404 no such order), and the 401 and 404 bodies are plain text. so json.loads runs only on the good path, status first, parse second. parse first and you get a JSON error that hides the real problem, the key. urlopen also raises HTTPError, (an error that stops the script) on any 4xx or 5xx, which is why the [try](./334-errors-in-scripts-catching-them-without-hiding-them.md) is there. the popular requests package does the opposite: a bad status comes back as a response, and raises only if you call raise_for_status().

timeout=5 gives up when the server stays silent for 5 seconds. without it urlopen waits forever on a silent server, so a nightly job never finishes. would you notice?

### check yourself

1. you delete the try and except from get, then call get("/orders/101", "k_report_7f3"), the key one character short. what does the call do?
<details><summary>answer</summary>

it raises HTTPError (HTTP Error 401) and the script stops there, so no tuple comes back and json.loads never runs. the tempting answer is (401, 'unknown caller'), but that tuple only exists because the except builds it.

</details>

2. the shop API answers 200 for order 101. your script runs print(data["customer_id"] + 1) on the parsed body. what prints?
```sql
SELECT customer_id FROM orders WHERE order_id = 101
```
<details><summary>answer</summary>

```result
customer_id
1
```

it prints 2. the JSON number came back as a python int, so the math works. the tempting answer is a TypeError, because os.environ values and csv values arrive as text, but JSON keeps its numbers.

</details>

---
prev: [342 environment variables, settings that live outside the code](./342-environment-variables-settings-that-live-outside-the-code.md) | next: not written yet
